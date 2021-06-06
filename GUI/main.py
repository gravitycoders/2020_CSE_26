import eel
import stream,encode,pydb
import auth
import os
from tkinter import filedialog
from tkinter import *
eel.init('web')




def StopCamera():
    stream.cap=False
    stream.name_list=[]
    
@eel.expose
def call_camera():
    eel.spawn(stream.StartCamera)
    print("Ended")
    

@eel.expose
def StopStream():
    eel.spawn(StopCamera)
    print('Stop')

@eel.expose
def verify_Login(email,password):
    rvar= auth.signin(email,password)
    eel.login_auth(rvar)

def update_user(ans):
    eel.updateuser(ans)

@eel.expose
def adduser(user,role):
    imgfile=None
    
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    imgfile=root.filename
    root.destroy()
    if imgfile!='':
        #create in DB
        uid,name=pydb.add_employee(user,role)
        print(uid,name)
        jsdoc=encode.imagencode(name,imgfile)
        res=pydb.add_face(uid,jsdoc)
        update_user(True)
    else:
        update_user(False)
    


eel.start('login.html')#,mode='None')