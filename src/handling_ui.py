import customtkinter as ctk
from customtkinter import *
from tkinter import *
import tkinter as tk
from handling_requests import *
from settings import *
from CTkTable import *
from PIL import Image
import base64
import io

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
        self.player_list = None
        self.player_on = None
        self.player_max = None
        
        # -- Eingabefeld animation
        self.min_width = 300
        self.max_width = 760
        self.step = 30
        self.anim_speed = 10
        self.current_width = self.min_width
        self.animating = {"running":False,"direction":None}
        # ---

        # --- Assets
        self.search_img = ctk.CTkImage(Image.open("assets/anonymous.png"),size=(40,40))
        self.row0 = ctk.CTkFrame(self.window,height=100,fg_color="transparent")
        self.row0.pack(fill="x",pady=0)
        self.eingabe_var = tk.StringVar()

        self.eingabe_feld = ctk.CTkEntry(master=self.row0, placeholder_text="Looking for a Server name ...",
        textvariable=self.eingabe_var,width=self.current_width,height=60,font=("opensans",30),)
        self.eingabe_feld.place(x=200,y=10,)

        self.suchen_btn = ctk.CTkButton(master=self.row0,text="Search",width=100,height=60,font=("opensans",30),
        command=lambda: self.getEingabe(),image=self.search_img,)
        self.suchen_btn.place(x=10,y=10)
        # -- unter Status oder host ip ,eula ,software oder so
        self.value = [["Status","Host","Port","Version","Players","IP","EULA Blocked"],
         [f"{self.status}",f"{self.host}",f"{self.port}",f"{self.version}",f"{self.player_list}",
         f"{self.ip}",f"{self.eula}"]]

        self.row1 = ctk.CTkFrame(master=self.window,fg_color="transparent")
        self.row1.pack(padx=0,pady=0)
        # -- Player list? Server Icon? MOTD, Plugins , Mods
        self.big_frame = ctk.CTkFrame(master=self.window,width=500,height=500)
        self.big_frame.pack(side=RIGHT,padx=15,pady=0)

        self.big_frame_2= ctk.CTkFrame(master=self.window,width=500,height=500)
        self.big_frame_2.pack(side=LEFT,padx=15,pady=0)

        self.table = CTkTable(master=self.row1, justify="center",header_color=nord["nord10"],
        row=2, column=7, values=self.value)
        self.table.pack(expand=True, padx=20, pady=10)
        # -- Server icon
        self.icon = ctk.CTkLabel(master=self.big_frame_2,text="",image=None,width=500,height=500,)
        self.icon.place(x=-180,y=-180)

        self.eingabe_feld.bind("<Enter>",lambda e: self.eingabe_anim(True))
        self.eingabe_feld.bind("<Leave>",lambda e: self.eingabe_anim(False))


        self.server_counter = 0
        self.frame_color = "#2E2E2E"

        self.color_config()

    def eingabe_anim(self,to_expand: bool):
        if self.animating["running"]:
            return  # Verhindert doppelte Animationen

        self.animating["running"] = True
        self.animating["direction"] = "expand" if to_expand else "shrink"

        def step_animation():
            if self.animating["direction"] == "expand" and self.current_width < self.max_width:
                self.current_width += self.step
                self.eingabe_feld.configure(width=self.current_width)
                self.eingabe_feld.focus()
                self.row0.after(self.anim_speed, step_animation)
            elif self.animating["direction"] == "shrink" and self.current_width > self.min_width:
                self.current_width -= self.step
                self.eingabe_feld.configure(width=self.current_width)
                self.row0.after(self.anim_speed, step_animation)
                self.eingabe_feld.master.focus_set()
            else:
                self.animating["running"] = False  # Animation fertig

        step_animation()

    def color_config(self):
        self.eingabe_feld.configure(fg_color=nord["nord1"])
        self.suchen_btn.configure(fg_color=nord["nord1"],hover_color=nord["nord2"])

        
    def getIcon(self,icon):
        icon_data = base64.b64decode(icon.split(",")[1])
        image_icon = ctk.CTkImage(Image.open(io.BytesIO(icon_data)),size=(100,100))
        return image_icon

    def getEingabe(self,):
        self.server_counter += 1
        eingabe = self.eingabe_var.get()
        host,port,ip,eula,version,status,player_list,player_on,player_max,server_icon = getData(self.url,eingabe) 

        self.player_list = ",".join(player_list)
        self.player_on = player_on
        self.player_max = player_max
        self.host = host
        self.port = port
        self.ip = ip
        self.eula = eula
        self.version = version
        self.status = status
        self.server_icon = server_icon

        image_icon = self.getIcon(self.server_icon)
        self.icon.configure(image=image_icon)


        if self.status:
            self.status = "Online"
        else:
            self.status = "Offline"
        if self.eula:
            self.eula = "Yes"
        else:
            self.eula = "No"

        self.table.delete_columns()
        self.table.delete_rows()
        self.table.insert(1,0,f"{self.status}")
        self.table.insert(1,2,f"{self.port}")
        self.table.insert(1,3,f"{self.version}")
        self.table.insert(1,4,f"{self.player_on}/{self.player_max}")
        self.table.insert(1,5,f"{self.ip}")
        self.table.insert(1,6,f"{self.eula}")
        self.table.insert(1,1,f"{self.host}")



        print(host,port)
        self.eingabe_feld.delete(0,tk.END)
