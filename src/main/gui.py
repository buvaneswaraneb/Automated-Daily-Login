import customtkinter
import tkinter
from PIL import Image
from py.db import DateDataBase
import os
import py.Pix as pix
from py.Accounts import getEmailList
import multiprocessing

BASE_DIR = os.path.dirname(__file__)
img_path_on = os.path.join(BASE_DIR,"asserts","images","on.png")
on_img  = customtkinter.CTkImage(light_image=Image.open(img_path_on),dark_image=Image.open(img_path_on),size=(40,40))

default_color = ("#E9BDFB","#33032F")
default_color_hover = ("#846C8E","#462C34")
textColor = ("black","white")
bg_color =  ("white","#170312")
customtkinter.set_appearance_mode("light")
class Window(customtkinter.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry("600x400")
        self.title('Pix Auto')
        self.con = content(self)
        self.con.pack(side="top",expand=True,fill="both")


class content(customtkinter.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.main()
        self.acc = False

         
    def main(self):
        self.side=SideMenu(self)
        self.side.pack(fill='y',side="left")
        self.home=MainMenu(self)
        self.home.pack(fill='both',side='left',expand=True)
        self.af = Historyframe(self)
        self.laf = AccountsPlaceHolder(self) #laf - list account Frame
        self.previousFrame = self.home


    def show_frame(self, frame_to_show):
        frames = [self.laf, self.af, self.home]

        if self.previousFrame == frame_to_show:
            frame_to_show.pack_forget()
            self.home.pack(fill="both", expand=True)  
            self.previousFrame = self.home
            return
        
        for frame in frames:
            frame.pack_forget()   # hide all frames

        frame_to_show.pack(fill="both", expand=True)  
        self.previousFrame = frame_to_show
    


class SideMenu(customtkinter.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = 0, border_width = None, bg_color = "transparent", fg_color = default_color, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.title = customtkinter.CTkLabel(master=self,text="Menu",text_color=textColor,width=150)
        self.title.pack(pady=10)
        s = SideMenuPlaceHolder(self)
        s.pack(side='top',fill="both",expand=True)
        self.author()
        
    def author(self):
        name = customtkinter.CTkLabel(text="Made By Soul",text_color=textColor,wraplength=100,master=self,font=('Inter',10))
        name.pack(side="bottom",pady=3)

class SideMenuPlaceHolder(customtkinter.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = default_color, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.menu()


         # SideMenuPlaceHolder → SideMenu → content
    def menu(self):
        button = customtkinter.CTkButton(master=self,text="Accounts",text_color=textColor,fg_color=bg_color,hover_color=default_color_hover,command=lambda:self.master.master.show_frame(self.master.master.laf))
        button.pack(side='top',pady=5)
        button = customtkinter.CTkButton(master=self,text="History",text_color=textColor,fg_color=bg_color,hover_color=default_color_hover,command=lambda:self.master.master.show_frame(self.master.master.af))
        button.pack(side='top',pady=5)
        

class MainMenu(customtkinter.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = 0, border_width = None, bg_color = "transparent", fg_color = bg_color, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.title = customtkinter.CTkLabel(text="Pix Auto",text_color=textColor,master=self)
        self.title.pack(pady=10,fill='x')
        self.start_button()
        self.alert_mess()
        self.switchButton()
        self.run_state = False
        self.process = None
    
    def check_process(self):

        if self.process is not None:
            if self.process.is_alive():
                self.after(200, self.check_process)
            else:
                print("Exit code:", self.process.exitcode)

                self.mess.configure(text="Process Finished", text_color="green")
                self.buttonStart.configure(state="normal")
                self.process = None
                self.run_state = False

    def run(self):
        self.run_state = not self.run_state
        if (self.run_state):
            self.mess.configure(text="Running",text_color="green")
            self.mess.pack()
            self.process = multiprocessing.Process(target=pix.main)
            self.process.start()
            self.buttonStart.configure(state="disabled")
            self.after(self.after(200, self.check_process))

        else:
            self.mess.configure(text="Not Running",text_color="red")
            self.mess.pack()
            if self.process is not None:
                    self.process.terminate()
                    self.process.join()
                    self.process = None
        
    def start_button(self):
        self.buttonStart = customtkinter.CTkButton(image=on_img,master=self,fg_color=default_color,height=200,width=200,corner_radius=200,hover_color=default_color_hover,text="",command=self.run,state="normal")
        self.buttonStart.pack(side='top',pady=30)

    def switchButton(self):
        self.var = customtkinter.StringVar(value="deafult")
        switch = customtkinter.CTkSwitch(master=self,onvalue="dark",offvalue='light',text="",command=self.view,variable=self.var)
        switch.pack(side="bottom", anchor="e", pady=10)
    
    def view(self):
        if (self.var.get() == "dark" and customtkinter.get_appearance_mode() == 'Dark'):
            customtkinter.set_appearance_mode("light")

        elif (self.var.get() == "dark"):
            customtkinter.set_appearance_mode("dark")
        elif (self.var.get() == "light"):
            customtkinter.set_appearance_mode("light")
        
    
    def alert_mess(self):
        self.mess = customtkinter.CTkLabel(text="Not Running", master=self,text_color="red")
        self.mess.pack(side = "top",pady=10)

class Historyframe(customtkinter.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = 0, border_width = None, bg_color = "transparent", fg_color = bg_color, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.text = customtkinter.CTkLabel(text="history", text_color=textColor,master=self)
        self.text.pack(side='top' , pady=10)

        # history scroll frame -> shows the 
        d = DateDataBase()
        li = d.getclaimedToday()
        self.placeholder = ScrollFrame(master=self,data=li)
        self.placeholder.emailPlaceHolder()
        self.placeholder.pack(side='top',expand=True,pady=10,fill='both')


class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, data,width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = bg_color, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.li =  data #["test","test","test"]
    
    def emailPlaceHolder(self):
        print(self.li)
        for mail in self.li:

            accountHolder = customtkinter.CTkFrame(master=self,
                                                   fg_color=default_color,
                                                   corner_radius=10)
            
            emailPlaceHolder = customtkinter.CTkFrame(master=accountHolder,
                                                      fg_color=default_color,
                                                      height=30,
                                                      corner_radius=10)
            
            statusPlaceHolder = customtkinter.CTkFrame(master=accountHolder,
                                                       fg_color=default_color,
                                                       height=30,
                                                       width=30,
                                                       corner_radius=10)
            
            self.mailLablel = customtkinter.CTkLabel(master=emailPlaceHolder,
                                                     text=mail,
                                                     text_color=textColor,
                                                     corner_radius=10,
                                                     fg_color=default_color,
                                                     height=30, 
                                                     justify="left",
                                                     anchor='w')
            
            claimed = customtkinter.CTkLabel(master=statusPlaceHolder,
                                             text="Claimed",
                                             text_color="green")
            
            emailPlaceHolder.pack(side="left",fill="both",expand=True)
            statusPlaceHolder.pack(side="left",fill="both",expand=True)
            self.mailLablel.pack(pady = 10 , padx =10, side = 'top')
            accountHolder.pack(pady = 10 , padx =10, side = 'top',fill='x',expand=True)
            claimed.pack(pady = 10 , padx =10, side = 'top')

    def noClaimEmailPlaceHolder(self):
            
            for mail in self.li:
                accountHolder = customtkinter.CTkFrame(master=self,
                                                       fg_color=default_color,
                                                       height=40)
                
                self.mailLablel = customtkinter.CTkLabel(master=accountHolder,
                                                        text=mail,
                                                        text_color=textColor,
                                                        corner_radius=5,
                                                        fg_color=default_color,
                                                        height=40,
                                                        justify="left",
                                                        anchor='w')
                
                self.mailLablel.pack(pady = 10, padx =10, side = 'top')
                accountHolder.pack(pady = 10 , padx =10, side = 'top',fill='x',expand=True)


class AccountsPlaceHolder(customtkinter.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = bg_color, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.title()
        self.accountList()


    def title(self):
        accTittle = customtkinter.CTkLabel(master=self,text="Accounts",text_color=textColor)
        accTittle.pack(side='top',pady=10)
    
    def accountList(self):
        li = getEmailList()
        print(li)
        s = ScrollFrame(master=self ,data=li)
        s.noClaimEmailPlaceHolder()
        s.pack(side='top',expand=True,pady=10,fill='both')


if __name__ == "__main__":
    w = Window()
    w.mainloop()