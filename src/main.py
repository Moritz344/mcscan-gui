from customtkinter import *
import customtkinter as ctk
from handling_ui import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MC Server Gui")
        self.geometry("1000x630")

        self.configure(fg_color="#2E2E2E")
        
        Main(self)



        self.mainloop()

App()
