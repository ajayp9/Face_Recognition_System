from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import face_recognition
import numpy as np
from time import strftime
from datetime import datetime

class Face_Recognition:
  def __init__(self,root):
    self.root=root
    self.root.geometry("1530x790+0+0")
    self.root.title("Face Recognition System")

    title_lbl=Label(self.root,text="FACE RECOGNITION",font=("times new roman",35,"bold"),bg="white",fg="darkgreen")
    title_lbl.place(x=0,y=0,width=1530,height=45)

    img_top=Image.open(r"college_images\face_detector1.Jpg")
    img_top=img_top.resize((650,700),Image.Resampling.LANCZOS)
    self.photoimg_top=ImageTk.PhotoImage(img_top)

    f_lbl=Label(self.root,image=self.photoimg_top)
    f_lbl.place(x=0,y=55,width=650,height=700)


    # 2ND IMAGE
    img_bottom=Image.open(r"college_images\facial_recognition_system_identification_digital_id_security_scanning_thinkstock_858236252_3x3-100740902-large.jpg")
    img_bottom=img_bottom.resize((950,700),Image.Resampling.LANCZOS)
    self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)

    f_lbl=Label(self.root,image=self.photoimg_bottom)
    f_lbl.place(x=650,y=55,width=950,height=700)


    # button
    b1_1=Button(f_lbl,text="face Recognition",cursor="hand2",command=self.face_recog,font=("times new roman",18,"bold"),bg="red",fg="white")
    b1_1.place(x=365,y=620,width=200,height=40)

  # Attendence....
  # def mark_attendance(self,i,r,n,d):
  #   with open("Ajay.csv","r+",newline="\n") as f:
  #     myDataList=f.readlines()
  #     name_list=[]
  #     for line in myDataList:
  #       entry=line.split((","))
  #       name_list.append(entry[0])
  #     if((i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list)) :
  #       now=datetime.now()
  #       d1=now.strftime("%d/%m/%Y")
  #       dtString=now.strftime("%H:%M:%S")
  #       f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")

  def mark_attendance(self,i,r,n,d):
    with open("Ajay.csv","r+",newline="\n") as f:
      myDataList=f.readlines()
      name_list=[]
      date_today=datetime.now().strftime("%d/%m/%Y")

      for line in myDataList:
        entry=line.split(",")
        if entry[0]==i and entry[5]==date_today:
          return 
        
      now=datetime.now()
      dtString=now.strftime("%H:%M:%S")
      f.writelines(f"\n{i},{r},{n},{d},{dtString},{date_today},Present")





  # face recognition.....
  def face_recog(self):
    def draw_boundray(img,classifier,scaleFactor,minNeighbours,color,text,clf):
      gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
      features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbours)

      coord=[]

      for (x,y,w,h) in features:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
        id,predict=clf.predict(gray_image[y:y+h,x:x+w])
        id = id + 21000
        confidence=int((100*(1-predict/300)))
        

       

        # mysql se data le rha hu
        try:
          conn=mysql.connector.connect(host="localhost",username="root",password="9936",database="face_recognizer")
          my_cursor=conn.cursor()

          # my_cursor.execute("select Name from student where Student_id="+str(id))
          # n=my_cursor.fetchone()
          # n="+".join(n)

          # my_cursor.execute("select Roll from student where Student_id="+str(id))
          # r=my_cursor.fetchone()
          # r="+".join(r)

          # my_cursor.execute("select Dep from student where Student_id="+str(id))
          # d=my_cursor.fetchone()
          # d="+".join(d)

          # my_cursor.execute("select Student_id from student where Student_id="+str(id))
          # i=my_cursor.fetchone()
          # i="+".join(i)

          def fetch_data(query, id):
            my_cursor.execute(query, (id,))
            result = my_cursor.fetchone()
            return result[0] if result is not None else "Unknown"

          # Usage
          n = fetch_data("SELECT Name FROM student WHERE Student_id=%s", id)
          r = fetch_data("SELECT Roll FROM student WHERE Student_id=%s", id)
          d = fetch_data("SELECT Dep FROM student WHERE Student_id=%s", id)
          i = fetch_data("SELECT Student_id FROM sTUDENT WHERE Student_id=%s",id)

          
          # print(f"Name: {n}, Roll: {r}, Department: {d}")

         

          if confidence>60:
            cv2.putText(img,f"ID:{i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,122,255),3)
            cv2.putText(img,f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,122,255),3)
            cv2.putText(img,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,122,255),3)
            cv2.putText(img,f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,122,255),3)
            self.mark_attendance(i,r,n,d)
          else:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
            cv2.putText(img,"Unknow Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
        except mysql.connector.Error as err:
          print(f"Error: {err}")
          cv2.putText(img, "Database Error", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 0), 3)

        coord=[x,y,w,h]

      return coord
    

    # function to face recognize
    def recognize(img,clf,faceCascade):
      coord=draw_boundray(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
      return img
    
    faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf=cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    video_cap=cv2.VideoCapture(0)



    while True:
      ret,img=video_cap.read()
      img=recognize(img,clf,faceCascade)
      cv2.imshow("Welcome To face Recognition",img)

      if cv2.waitKey(1)==13:
        break
    video_cap.release()
    cv2.destroyAllWindows()




if __name__=="__main__":
  root=Tk()
  obj=Face_Recognition(root)
  root.mainloop()
