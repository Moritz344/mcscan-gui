import customtkinter as ctk
from customtkinter import *
from tkinter import *
import tkinter as tk
from handling_requests import *
from tkhtmlview import HTMLLabel

class Main():
    def __init__(self,window):

        self.master = self
        self.window = window
        
        self.url = f"https://api.mcstatus.io/v2/widget/java/"
        
        self.row0 = ctk.CTkFrame(self.window,height=100,fg_color="transparent")
        self.row0.pack(fill="x",pady=0)
        self.eingabe_var = tk.StringVar()
        self.eingabe_feld = ctk.CTkEntry(master=self.row0, placeholder_text="Looking for a Server name ...",
        textvariable=self.eingabe_var,width=970,height=60,font=("opensans",30),)
        self.eingabe_feld.pack(padx=10,pady=10)

        self.suchen_btn = ctk.CTkButton(master=window,text="Suchen",width=100,
        command=lambda: self.getEingabe())

        self.server_counter = 0
        self.frame_color = "#2E2E2E"
        
        # --- Zwei Reihen erstellen für pack 
        self.row1 = ctk.CTkFrame(self.window,fg_color="transparent")
        self.row1.pack(fill="x", pady=20)

        self.card_1 = ctk.CTkFrame(master=self.row1,width=350,height=250,corner_radius=30,)
        self.card_1.pack(side="left", expand=True, padx=20,pady=10)

        self.card_2 = ctk.CTkFrame(master=self.row1,width=350,height=250,corner_radius=30)
        self.card_2.pack(side="left", expand=True, padx=0,pady=10)

        # --- Zweite Reihe
        self.row2 = ctk.CTkFrame(self.window,fg_color="transparent")
        self.row2.pack(fill="x", pady=20)

        self.card_3 = ctk.CTkFrame(master=self.row2,width=350,height=250,corner_radius=30)
        self.card_4 = ctk.CTkFrame(master=self.row2,width=350,height=250,corner_radius=30)

        self.card_3.pack(in_=self.row2, side="left", expand=True, padx=40)
        self.card_4.pack(in_=self.row2, side="left", expand=True, padx=40)
        

    def getEingabe(self,):
        self.server_counter += 1
        eingabe = self.eingabe_var.get()
        getData(self.url,eingabe) # DEBUG
        image_url = f"{self.url}{eingabe}"
        
        
        #my_label = HTMLLabel(self.frame,html=f"""
        #    <img src={image_url} >
        #""",width=400,height=100)
        #my_label.place(x=0,y=0)
        print("DEBUG",self.url + eingabe)
