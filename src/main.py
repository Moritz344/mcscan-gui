from customtkinter import *
import customtkinter as ctk
from handling_ui import *
from start_screen import *
from settings import *
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MC Server Gui")
        self.geometry("1000x700")
        self.minsize(1000,700)
        self.maxsize(1000,700)
        self.iconbitmap("assets/app-icon.ico")


        self.configure(fg_color=nord["nord0"])
        Main(self)



        self.mainloop()

Startscreen()
App()
