from customtkinter import *
from PIL import Image
import smtplib
import os, sys

def resource_path(relative_path): # A FUNCTION TO COUNTER THE ERRORS FOR ADDITIONAL FILES WHEN ADDED IN PYINSTALLER
    # (https://youtu.be/xJAM8_Lx5mY?t=906) Thanks to this video!!
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path,relative_path)

app = CTk()
app.title("Mailer - Login")
app.geometry("800x600")
app.iconbitmap(resource_path("./assets/icon.ico"))
set_appearance_mode('dark')
side_img = Image.open(resource_path("./assets/side.jpg"))

CTkLabel(master=app, text="", image=CTkImage(dark_image=side_img,light_image=side_img,size=(400,600))).place(x=400,y=0)

img1= Image.open(resource_path("./assets/email-icon.png"))
img2 = Image.open(resource_path("./assets/pass-icon.png"))
img3 = Image.open(resource_path("./assets/arrow.png"))

frame = CTkFrame(master=app,height=600,width=400,border_width=2)
frame.place(x=0,y=0)

label = CTkLabel(master=frame,text='Mailer',font=("calibri",40,'bold','italic'),bg_color="transparent")
label.place(x=150,y=50)

label_email = CTkLabel(master=frame,text='  Email:',anchor="w", justify="left",font=("calibri",20),bg_color="transparent",image=CTkImage(dark_image=img1, light_image=img1, size=(20,20)), compound="left")
label_email.place(x=50,y=150)
email = CTkEntry(master=frame,placeholder_text='Enter your mail...',font=("Arial",20),width=300,height=50,corner_radius=20)
email.place(x=50,y=180)

# Function for show security key
count = 0
def show():
    global count
    if(count % 2 == 0):
       key.configure(show = "")
    else:
        key.configure(show = '*')
    count+=1
    
label_pass = CTkLabel(master=frame,text='  Security key:',anchor="w", justify="left",font=("calibri",20),bg_color="transparent",image=CTkImage(dark_image=img2, light_image=img2, size=(20,20)), compound="left")
label_pass.place(x=50,y=260)
key = CTkEntry(master=frame,placeholder_text='Enter your app security key...',show="*",font=("Arial",20),width=300,height=50,corner_radius=20)
key.place(x=50,y=290)
show_pass = CTkCheckBox(master=frame,text='Show security key',width=30,height=30,corner_radius=10,font=("calibri",16),command=show)
show_pass.place(x=50, y=350)

# Login function, connecting to server and then creating a new window for sending mail
def login():
    
    global sender_email
    sender_email = email.get()

    global login_key
    login_key = key.get()

    try:
        global server
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender_email,login_key) 
    except:
        warning = CTkLabel(master=frame,text='Wrong Credentials',font=("calibri",20),text_color="Red")
        warning.place(x=190,y=260)
        return
    
    app.destroy()
    w = CTk()  
    w.geometry("800x600")
    w.title('Mailer')
    w.iconbitmap(resource_path("./assets/icon.ico"))

    label = CTkLabel(master=w,text='Mailer',font=("calibri",40,'bold','italic'),bg_color="transparent")
    label.place(x=350,y=50)

    recp = CTkEntry(master=w,placeholder_text='Recipient',font=("Arial",20),width=300,height=50,corner_radius=20)
    recp.place(x=270,y=150)

    subj = CTkEntry(master=w,placeholder_text='Subject',font=("Arial",20),width=300,height=50,corner_radius=20)
    subj.place(x=270,y=220)

    body = CTkTextbox(master=w,width=300,height=200,border_color="#000000",border_width=2,corner_radius=20)
    body.place(x=270,y=280)
    
    def send_mail():
        temp = CTkLabel(master=w,text="",font=("calibri",20))
        temp.place(x=270,y=110)
        try:
           recipient = recp.get()
           data = f"Subject: {subj.get()}\n\n{body.get('0.0','end')}"
           server.sendmail(sender_email,recipient,data)
           temp.configure(text="STATUS: Successfully sent!",text_color="Green")
        except:
            temp.configure(text="STATUS: Error occured!",text_color="Red")

    btn_send = CTkButton(master=w,text="Send",font=("Arial",20),height=50,width=70,corner_radius=20,command=send_mail)
    btn_send.place(x=350,y=500)

    cmb = CTkComboBox(master=w,values=["Dark","Light","System"],width=150,height=30,corner_radius=10,command=set_appearance_mode)
    cmb.place(x=20,y=550)
    cmb.set("Dark")

    w.mainloop()

btn = CTkButton(master=frame,text="",image=CTkImage(light_image=img3,dark_image=img3,size=(50,50)),anchor="center",font=("Arial",30),height=50,width=70,corner_radius=100,command=login)
btn.place(x=130,y=440)

cmb = CTkComboBox(master=frame,values=["Dark","Light","System"],width=150,height=30,corner_radius=10,command=set_appearance_mode)
cmb.place(x=20,y=550)
cmb.set("Dark")

app.mainloop()

'''
from customtkinter import *

app = CTk()
app.geometry("800x600")

def select_file():
    filename = filedialog.askopenfile() #askdirectory
    print(filename)

btn = CTkButton(master=app,text="Attach",command=select_file)
btn.place(x=400,y=300)

app.mainloop()
'''