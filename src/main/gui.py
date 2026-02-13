import customtkinter
import Pix

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("PIX AI Login AUTOMATION")

    def main(self):
        self.text()
        self.rnBtn()
    
    def text(self):
        tittle = "PixAi AutoMated Login"
        text = customtkinter.CTkLabel(self,text=tittle,fg_color="transparent",anchor="center")
        text.pack(pady=30)
        self.label = customtkinter.CTkLabel(self,text="",height=50,width=200)
        self.label.pack(pady=20)
    
    def rnBtn(self):
        btn = "Run"
        button = customtkinter.CTkButton(self,text=btn,height=50,width=120,corner_radius=20,command=self.run)
        button.pack()

    #logic
    def run(self):
        Status = "Running Please wait"
        self.label.configure(text=Status)
        completed = Pix.main()
        if (completed):
            Status = "Sucessfully Completed"
            self.label.configure(Status)
            
    





app = App()
app.main()
app.mainloop()