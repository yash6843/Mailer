from customtkinter import *

app = CTk()
app.geometry("800x600")

def select_file():
    filename = filedialog.askopenfile() #askdirectory
    print(filename)

btn = CTkButton(master=app,text="Attach",command=select_file)
btn.place(x=400,y=300)

app.mainloop()