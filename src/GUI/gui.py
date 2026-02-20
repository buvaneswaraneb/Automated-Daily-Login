import customtkinter
from PIL import Image
import os
from  main.db import Date
from main.Pix import main 

#==================Path======================#
BASE_DIR = os.path.dirname(__file__)
img_path_on = os.path.join(BASE_DIR,"asserts","images","on.png")
on_img  = customtkinter.CTkImage(light_image=Image.open(img_path_on),dark_image=Image.open(img_path_on),size=(40,40))

#=============== Colors ================== #
default_color = ("#33032F","#E9BDFB")
default_color_hover = "#846C8E"
textColor = ("white","black")
bg_color =  ("#170312","white")

class Window(customtkinter.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry("600x400")
        self.title('Pix Auto')
        self._set_appearance_mode('default')
        self.main()
    
    def main(self):
        self.side=SideMenu(self)
        self.side.pack(fill='y',side="left")
        self.home=MainMenu(self)
        self.home.pack(fill='both',side='left',expand=True)

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

    def accbtn(self):
        pass

    def menu(self):
        button = customtkinter.CTkButton(master=self,text="Accounts",text_color=textColor,fg_color=bg_color,hover_color="#E3D8E3")
        button.pack(side='top')

class MainMenu(customtkinter.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = 0, border_width = None, bg_color = "transparent", fg_color = bg_color, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.title = customtkinter.CTkLabel(text="Pix Auto",text_color=textColor,master=self)
        self.title.pack(pady=10,fill='x')
        self.start_button()
        self.alert_mess()
        self.switchButton()
        self.run_state = False

    def run(self):
        self.run_state = not self.run_state
        if (self.run_state):
            self.mess.configure(text="Running",text_color="green")
            self.mess.pack()
            main()

        else:
            self.mess.configure(text="Not Running",text_color="red")
            self.mess.pack()
        
    def start_button(self):
        buttonStart = customtkinter.CTkButton(image=on_img,
                                         master=self,fg_color=default_color,
                                         height=200,
                                         width=200,
                                         corner_radius=200,
                                         hover_color=default_color_hover,
                                         text="",
                                         command=self.run)
        buttonStart.pack(side='top',pady=30)

    def switchButton(self):
        self.var = customtkinter.StringVar(value="deafult")
        switch = customtkinter.CTkSwitch(master=self,onvalue="dark",offvalue='light',text="")
        switch.pack(side='right')
    
    def alert_mess(self):
        self.mess = customtkinter.CTkLabel(text="Not Running", master=self,text_color="red")
        self.mess.pack(side = "top",pady=10)

Window().mainloop()