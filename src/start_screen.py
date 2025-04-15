from customtkinter import *
import customtkinter as ctk
import sys
from settings import *
from PIL import Image
from CTkToolTip import *

# TODO: button animation

class Startscreen(object):
    def __init__(self):
        super().__init__()

        self.window = ctk.CTk()
        self.window.maxsize(800,600)
        self.window.minsize(800,600)
        self.window.iconbitmap("assets/app-icon.ico")

        self.window.geometry("800x600")
        self.window.title("mcscan")
        self.window.configure(fg_color=eerie_black)

        github_img = ctk.CTkImage(Image.open("assets/github.png"),size=(70,70))
        github_label = ctk.CTkLabel(self.window,text="",image=github_img)
        github_label.place(x=10,y=510)

        self.button_frame = ctk.CTkFrame(self.window,width=300,height=500,fg_color="transparent",)
        self.button_frame.place(x=180,y=400)
        
        app_frame = ctk.CTkFrame(self.window,width=300,height=300,corner_radius=10)
        app_frame.place(x=240,y=60)
        app_img = ctk.CTkImage(Image.open("assets/app_img.png"),size=(300,300))
        app_label = ctk.CTkLabel(app_frame,text="",image=app_img,)
        app_label.place(x=0,y=0)

        tooltip_github = CTkToolTip(github_label,delay=0.3,message="github.com/Moritz344")

        def start_app():
            self.window.destroy()

        self.current_width = 200
        self.current_height = 50
        self.start_btn = ctk.CTkButton(
            master=self.button_frame,
            text="Start",
            width=self.current_width,
            height=self.current_height,
            font=("opensans",50),
            fg_color=nord["nord14"],
            command=start_app,

        )
        


        self.start_btn.pack(side=LEFT,expand=True,padx=10)

        quit_btn = ctk.CTkButton(
            master=self.button_frame,
            text="Quit",
            width=200,
            height=50,
            font=("opensans",50),
            fg_color=nord["nord11"],
            command=lambda: sys.exit(),

        )


        quit_btn.pack(side=RIGHT,expand=True)

        self.window.protocol("WM_DELETE_WINDOW",lambda: sys.exit())



        self.window.mainloop()

