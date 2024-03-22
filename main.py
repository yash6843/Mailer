from customtkinter import *
from PIL import Image
from CTkToolTip import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

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
img4 = Image.open(resource_path("./assets/icon.ico"))
img5 = Image.open(resource_path("./assets/attach.png"))

frame = CTkFrame(master=app,height=600,width=400,border_width=2)
frame.place(x=0,y=0)

label = CTkLabel(master=frame,text='  Mailer',compound="left",font=("calibri",40,'bold','italic'),image=CTkImage(dark_image=img4, light_image=img4, size=(40,40)),bg_color="transparent")
label.place(x=100,y=50)

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

    label = CTkLabel(master=w,text='  Mailer',compound="left",image=CTkImage(dark_image=img4, light_image=img4, size=(40,40)),font=("calibri",40,'bold','italic'),bg_color="transparent")
    label.place(x=300,y=50)

    recp = CTkEntry(master=w,placeholder_text='Recipient',font=("Arial",20),width=300,height=50,corner_radius=20)
    recp.place(x=270,y=150)

    tooltip = CTkToolTip(recp, message="Differentiate multiple mails using \",\"\n Example: abc@gmail.com , xyz@gmail.com")
   
    try:
         recp.bind("<Enter>", tooltip.show)
         recp.bind("<Leave>", tooltip.hide)
    except:
        pass

    subj = CTkEntry(master=w,placeholder_text='Subject',font=("Arial",20),width=300,height=50,corner_radius=20)
    subj.place(x=270,y=220)

    body = CTkTextbox(master=w,width=300,height=200,border_color="#000000",border_width=2,corner_radius=20)
    body.place(x=270,y=280)
    
    files = []
    def attach_file():
         file = filedialog.askopenfile(title="Attach file")
         files.insert(0,file.name)

    def send_mail():
        subject = subj.get()
        content = body.get('0.0','end')
        recipients = (recp.get()).split(",")

        temp = CTkLabel(master=w,text="",font=("calibri",20))
        temp.place(x=270,y=110)

        try:
            for recp_email in recipients:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recp_email
                msg['Subject'] = subject
                msg.attach(MIMEText(content, 'plain'))
            
                for filename in  files:
                    name = (filename.split("/"))[-1]
                    attachment= open(filename, 'rb')  # r for read and b for binary
                    attachment_package = MIMEBase('application', 'octet-stream')
                    attachment_package.set_payload((attachment).read())
                    encoders.encode_base64(attachment_package)
                    attachment_package.add_header('Content-Disposition', "attachment; filename= " + name)
                    msg.attach(attachment_package)
            
            text = msg.as_string()
            server.sendmail(sender_email, recp_email, text)
            print(f"Mail sent to {recp_email}")
            temp.configure(text="STATUS: Successfully sent!",text_color="Green")
            
        except:
            temp.configure(text="STATUS: Error occured!",text_color="Red")

    btn_attach = CTkButton(master=w,text="",height=30,width=30,corner_radius=100,image=CTkImage(dark_image=img5, light_image=img5, size=(30,30)),bg_color="transparent",command=attach_file)
    btn_attach.place(x=450,y=500)

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