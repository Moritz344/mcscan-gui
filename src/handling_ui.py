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
import CTkMessagebox
from CTkToolTip import *


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

        self.icon_frame = ctk.CTkFrame(self.window,width=150,height=150,fg_color="transparent",)
        self.motd_frame = ctk.CTkFrame(master=self.window,width=400,height=146,)

        self.icon_frame.place(x=20,y=180)

        self.motd_label = ctk.CTkLabel(self.motd_frame,text="",corner_radius=10,
        bg_color=f"{eerie_black}",width=400,height=150,font=("opensans",20))
        
        self.motd_label.place(x=0,y=0)
        
        self.mods_frame = ctk.CTkFrame(self.window,width=540,height=95,border_width=5,corner_radius=0,fg_color="#1e293b",border_color="#334155")
        self.mods_header = ctk.CTkFrame(self.window,width=540,height=70,fg_color="#334155",corner_radius=0)

        self.mods_label = ctk.CTkTextbox(self.mods_frame,width=530,height=90,font=("opensans",20),activate_scrollbars=True,fg_color="transparent")
        self.mods_label.place(x=4,y=0)

        self.plugin_frame = ctk.CTkFrame(self.window,width=540,height=150,border_width=5,corner_radius=0,fg_color="#1e293b",border_color="#334155")
        self.plugin_header = ctk.CTkFrame(self.window,width=540,height=50,fg_color="#334155",corner_radius=0)

        self.plugins_label = ctk.CTkTextbox(self.plugin_frame,width=530,height=130,font=("opensans",20),fg_color="transparent")
        self.plugins_label.place(x=4,y=10)

        self.player_frame = ctk.CTkFrame(self.window,width=410,height=390,border_width=5,corner_radius=0,fg_color="#1e293b",border_color="#334155")
        self.player_header = ctk.CTkFrame(self.window,width=410,height=100,fg_color="#334155",corner_radius=0)

        self.player_label = ctk.CTkTextbox(self.player_frame,width=390,height=370,font=("opensans",20),fg_color="transparent")
        self.player_label.place(x=4,y=10)

        self.table = CTkTable(master=self.row1, justify="center",header_color=nord["nord3"],
        row=2, column=7, colors=["#1e293b","#1e293b"],values=self.value,corner_radius=0,height=30,font=("opensans",16),)
        self.table.pack(expand=True, padx=20, pady=10)
        # -- Server icon
        self.icon = ctk.CTkLabel(master=self.icon_frame,text="",image=None,width=500,height=500,)
        self.icon.place(x=-180,y=-180)

        self.eingabe_feld.bind("<Enter>",lambda e: self.eingabe_anim(True))
        self.eingabe_feld.bind("<Leave>",lambda e: self.eingabe_anim(False))

        self.frame_color = "#2E2E2E"

        self.player_info = ctk.CTkLabel(self.window,text="shows a max of 12 players.",text_color="grey",
        font=("opensans",15),fg_color="transparent",height=10)
            
        self.placeholder_frame = ctk.CTkFrame(self.window,width=1000,corner_radius=10,fg_color="transparent")
        self.placeholder_frame.place(x=300,y=230)
        placeholder_image = ctk.CTkImage(Image.open("assets/404.png"),size=(200,200))
        self.placeholder_label = ctk.CTkLabel(self.placeholder_frame,text="",image=placeholder_image,)
        self.placeholder_label.place(x=0,y=30)
        self.placeholder_text = ctk.CTkLabel(self.placeholder_frame,text="Nothing here yet.",font=("opensans",50))
        self.placeholder_text.pack(pady=200,side= TOP )
        
        # -- creating tags for color
        self.mods_label.tag_config("warning_tag",foreground=nord["nord11"])
        #self.player_label.tag_config("warning_tag",foreground=nord["nord11"])
        self.plugins_label.tag_config("warning_tag",foreground=nord["nord11"])

        # ---

        # -- tooltips
        self.tooltip_1 = CTkToolTip(self.icon,delay=0.3,message="No Icon found")
        self.tooltip_2 = CTkToolTip(self.suchen_btn,delay=0.5,message="Look for Server")
        
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
        self.suchen_btn.configure(fg_color=nord["nord1"],hover_color=nord["nord3"])

        
    def getIcon(self,icon,icon_name):
        try:
            icon_data = base64.b64decode(icon.split(",")[1])
            image_icon = ctk.CTkImage(Image.open(io.BytesIO(icon_data)),size=(150,150))
            self.icon_status = True
            return image_icon,self.icon_status
        except Exception :
            CTkMessagebox.CTkMessagebox(self.window,
            message="Icon not found",icon="warning",title="Icon",font=("opensans",15))
            print("DEBUG: Wenn Icon 'None' ist kann dieser fehler kommen",)
            image_icon = ctk.CTkImage(Image.open("assets/question-sign.png"),size=(100,100))
            self.icon_status = False
            return image_icon,self.icon_status

    def getEingabe(self,):

        self.motd_frame.place(x=160,y=180)

        self.player_info.place(x=580,y=670)

        self.mods_header.place(x=20,y=340)
        self.mods_frame.place(x=20,y=410)

        self.plugin_header.place(x=20,y=520)
        self.plugin_frame.place(x=20,y=520)

        self.player_header.place(x=570,y=180)
        self.player_frame.place(x=570,y=280)

        self.plugin_icon = ctk.CTkImage(Image.open("assets/plugin.png"),size=(30,30))
        ctk.CTkLabel(self.plugin_header,compound="left",image=self.plugin_icon,text=" Plugins List",font=("opensans",30,)).place(x=10,y=5)
        
        self.player_icon = ctk.CTkImage(Image.open("assets/profile.png"),size=(80,80))
        ctk.CTkLabel(self.player_header,compound="left",image=self.player_icon,text=" Player List",font=("opensans",60)).place(x=10,y=5)

        self.mod_icon = ctk.CTkImage(Image.open("assets/puzzle.png"),size=(50,50))
        ctk.CTkLabel(self.mods_header,compound="left",image=self.mod_icon,text=" Mods List",font=("opensans",40)).place(x=10,y=10)
        self.mods_label.configure(state="normal")
        self.player_label.configure(state="normal")
        self.plugins_label.configure(state="normal")
        self.placeholder_text.pack_forget()
        self.placeholder_label.place_forget()
        self.placeholder_frame.place_forget()

        eingabe = self.eingabe_var.get()

        try:
            host,port,ip,eula,version,status,player_list,player_on,player_max,server_icon,motd,mods_list,plugins_list = getData(self.url,eingabe) 



            self.player_list = ",\n".join(player_list)
            self.player_on = player_on
            self.player_max = player_max
            self.host = host
            self.port = port
            self.ip = ip
            self.eula = eula
            self.version = version
            self.status = status
            self.server_icon = server_icon
            self.icon_status: None = None
            self.motd = motd
            self.mods = ",\n".join(mods_list)
            self.plugins = ",\n".join(plugins_list)


            # -- motd text
            print(len(self.motd))
            if len(self.motd) > 56:
                self.motd_label.configure(font=("opensans",18))
            elif len(self.motd) <= 56:
                self.motd_label.configure(font=("opensans",20))

            self.motd_label.configure(text=self.motd)
            # -- löschen von vorherigen eingaben
            self.mods_label.delete(1.0,tk.END)
            self.player_label.delete(1.0,tk.END)
            self.plugins_label.delete(1.0,tk.END)
            # --
            if self.mods != "":
                self.mods_label.insert(1.0,f"""{self.mods}""")
            else:
                self.mods_label.insert(1.0,"""
I wasn't able to obtain this information.""","warning_tag")



            image_icon,self.icon_status = self.getIcon(self.server_icon,self.icon_status)
            self.icon.configure(image=image_icon,)
            if not self.icon_status:
                self.tooltip_1.configure(message="Icon not found")
            else:
                self.tooltip_1.configure(message=f"Server icon from: {self.host} ")
            
            if self.player_list != "":
                self.player_label.insert(1.0,f"""{self.player_list}""")
            else:
                self.player_label.insert(1.0,""" \n
I wasn't able to obtain this information.""","warning_tag")
            if self.plugins != "":
                self.plugins_label.insert(1.0,f"""{self.plugins}""")
            else:
                self.plugins_label.insert(1.0,""" \n
I wasn't able to obtain this information.""","warning_tag")

            # -- Textbox deaktivieren nach einfügen
            self.mods_label.configure(state="disabled")
            self.player_label.configure(state="disabled")
            self.plugins_label.configure(state="disabled")
#
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



            #self.motd_label.configure(bg_color=eerie_black)
            self.eingabe_feld.delete(0,tk.END)

        except Exception as e:
            image_icon = ctk.CTkImage(Image.open("assets/question-sign.png"),size=(100,100))
            self.icon.configure(image=image_icon,)
            CTkMessagebox.CTkMessagebox(self.window,message="This Server does not exist",
            icon="warning",title="Invalid Server Name",font=("opensans",15))
            self.eingabe_feld.delete(0,tk.END)
            print(e)
