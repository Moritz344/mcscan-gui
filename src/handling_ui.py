import customtkinter as ctk
from customtkinter import *
from tkinter import *
import tkinter as tk
from handling_requests import *
from tkhtmlview import HTMLLabel
from PIL import Image,ImageTk
from settings import *
from CTkTable import *

class Main():
    def __init__(self,window):

        self.master = self
        self.window = window
        
        self.url = f"https://api.mcstatus.io/v2/status/java/"
        self.host = None
        self.port = None
        self.ip = None
        self.eula = None
        self.version = None
        self.status = None

        # --- Assets
        self.search_img = ctk.CTkImage(Image.open("assets/search.png"),size=(30,30))
        
        self.row0 = ctk.CTkFrame(self.window,height=100,fg_color="transparent")
        self.row0.pack(fill="x",pady=0)
        self.eingabe_var = tk.StringVar()
        self.eingabe_feld = ctk.CTkEntry(master=self.row0, placeholder_text="Looking for a Server name ...",
        textvariable=self.eingabe_var,width=770,height=60,font=("opensans",30),)
        self.eingabe_feld.pack(padx=20,pady=10,side=RIGHT,expand=True)

        self.suchen_btn = ctk.CTkButton(master=self.row0,text="Search",width=100,height=70,font=("opensans",30),
        command=lambda: self.getEingabe(),image=self.search_img,)
        self.suchen_btn.pack(padx=10,pady=0,expand=True)
        
        # -- unter Status oder host ip ,eula ,software oder so
        self.value = [["Status","Host","Port","Version","Players","Mods","Plugins"],
         [f"{self.status}",f"{self.host}",f"{self.port}",f"{self.version}",""],
         ["","","","",""],
         ["","","","",""],
         ["","","","",""]]

        self.table = CTkTable(master=self.window, justify="center",header_color=nord["nord10"],
        row=5, column=7, values=self.value)
        self.table.pack(expand=True, fill="both", padx=20, pady=20)


        self.server_counter = 0
        self.frame_color = "#2E2E2E"
        

        self.color_config()
        
    def color_config(self):
        

        self.eingabe_feld.configure(fg_color=nord["nord1"])
        self.suchen_btn.configure(fg_color=nord["nord1"])

    def getEingabe(self,):
        self.server_counter += 1
        eingabe = self.eingabe_var.get()
        host,port,ip,eula,version,status = getData(self.url,eingabe) # DEBUG
        
        
        self.host = host
        self.port = port
        self.ip = ip
        self.eula = eula
        self.version = version
        self.status = status

        self.table.delete_columns()
        self.table.delete_rows()
        self.table.insert(1,0,f"{self.status}")
        self.table.insert(1,2,f"{self.port}")
        self.table.insert(1,3,f"{self.version}")
        self.table.insert(1,1,f"{self.host}")



        print(host,port)
        self.eingabe_feld.delete(0,tk.END)
