import customtkinter
from PIL import Image
import tkinter

app = customtkinter.CTk()
app.title("Trying Out")
app.geometry("600x400")
app.resizable(height=True,width=True)
on = False
scene = 0
default_font = None
theme_color = "#E9BDFB"


def changestate():
    global on
    on = not on
    if on :
        below_text.configure(
            text="Running",
            text_color = "green",
        )
    else:
            below_text.configure(
            text="Not Running",
            text_color = "red",
        )
            

#main Frame 
bg_frame = customtkinter.CTkFrame(master=app,fg_color="#E9BDFB",width=150,corner_radius=0)
bg_frame.pack(side='left',fill='y')
#side Frame
bg_frame_W = customtkinter.CTkFrame(master=app,fg_color="white",corner_radius=0)
bg_frame_W.pack(side='right',fill='both',expand=True)

#blank
account_frame = customtkinter.CTkFrame(master=app,fg_color="white",corner_radius=0)
account_frame.pack(side='right',fill='both',expand=True)
account_frame.forget()

scenes = [bg_frame_W,account_frame]

changebg = False
def accountScreen():
    global changebg
    changebg = not changebg
    if (changebg):
        scenes[0].forget()
        scenes[1].tkraise()
        scenes[1].pack(side='right',fill='both',expand=True)
        return
    scenes[1].forget()
    scenes[0].tkraise()
    scenes[0].pack(side='right',fill='both',expand=True)

#pixAi title
title = customtkinter.CTkLabel(text="Pix Auto",master=bg_frame_W,text_color='black')
title.pack(pady=20,side='top')
#buttonimg
img = Image.open("test/on.png")
img = customtkinter.CTkImage(img)
#startbutton
start = customtkinter.CTkButton(image=img,text="",height=200,width=200,master=bg_frame_W,corner_radius=200,fg_color="#E9BDFB",hover_color="#855D95",command=changestate)
start.pack(pady=20)
#status 
below_text = customtkinter.CTkLabel(text="Not Running",text_color="red",master=bg_frame_W)  
below_text.pack()
#menu
menu_text = customtkinter.CTkLabel(text="Menu" ,text_color="black",master=bg_frame,width=150)
menu_text.pack(side ="top",fill ='both',pady=20)
#sideMenu
side_menu = customtkinter.CTkFrame(master=bg_frame,fg_color="transparent")
side_menu.pack(side='top')
#accounts menu
accountsbtn = customtkinter.CTkButton(text="Accounts",text_color="black",master=side_menu,fg_color='white',hover_color="#ECDDF1",command=accountScreen)
accountsbtn.pack(side='top')
#addAccount
addAccount = customtkinter.CTkButton(text="Add Account",text_color="black",master=side_menu,fg_color='white',hover_color="#ECDDF1")
addAccount.pack(side='top',pady=10)

#Account frame :

account_frame.columnconfigure(index=(0,1,2,3,4),weight=1)
account_frame.rowconfigure(index=(0,2,3,4,5,6),weight=2)
account_frame.rowconfigure(index=1,weight=2)
header_text = customtkinter.CTkLabel(text="Accounts",text_color="black",master=account_frame)
header_text.grid(column=2,row=0,sticky='ewn', pady=20)

email_frame = customtkinter.CTkFrame(master=account_frame)
email_frame.grid(column=0,row=1,rowspan=7,columnspan=5,sticky='nsew')

# email_label = customtkinter.CTkLabel(master=email_frame,text=email_present[0],corner_radius=10,fg_color=theme_color,text_color="black")
# email_label.pack(side='top',fill='x',pady=10,padx=10)

app.mainloop()