import customtkinter
from PIL import Image

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("PIX AI Login AUTOMATION")
        self.head = False
        customtkinter.set_appearance_mode("light")
        self.hdlessTxT = "ON"
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
    def main(self):
        self.homepage()

    def homepage(self):
        title = "Pix Auto"
        title_lablel = customtkinter.CTkLabel(self, text=title, text_color="Black",font=('Inter',24))
        title_lablel.pack()
        on_img_svg = Image.open("src/main/GUI/asserts/images/on.png")
        on_img = customtkinter.CTkImage(dark_image=on_img_svg,size=(100,100))
        turn_on = customtkinter.CTkButton(self,text="", height= 250 ,width= 250 ,image=on_img ,corner_radius= 400,fg_color="#E9BDFB",hover="#935858")
        turn_on.pack()
        sidemenu = customtkinter.CTkLabel(self,text="",height=570,width=200,fg_color="#E9BDFB",corner_radius=50)
        sidemenu.pack()




app = App()
app.main()
app.mainloop()
