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

# TODO: App icon

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
        # 15 200
        self.frame_x_2 = 1200
        self.big_frame = ctk.CTkFrame(master=self.window,width=500,height=500)
        self.big_frame.place(x=self.frame_x_2,y=200)

        self.frame_x = 1000
        self.big_frame_2= ctk.CTkFrame(master=self.window,width=500,height=500)
        self.big_frame_2.place(x=self.frame_x,y=0)

        self.table = CTkTable(master=self.row1, justify="center",header_color=nord["nord10"],
        row=2, column=7, values=self.value)
        self.table.pack(expand=True, padx=20, pady=10)
        # -- Server icon
        self.icon = ctk.CTkLabel(master=self.big_frame_2,text="",image=None,width=500,height=500,)
        self.icon.place(x=-180,y=-180)

        self.eingabe_feld.bind("<Enter>",lambda e: self.eingabe_anim(True))
        self.eingabe_feld.bind("<Leave>",lambda e: self.eingabe_anim(False))


        self.big_frame.configure(width=400)

        self.server_counter = 0
        self.frame_color = "#2E2E2E"

        # -- Labels for big frame 2
        self.motd_label = ctk.CTkLabel(self.big_frame_2,text="",corner_radius=10,
        bg_color=f"{eerie_black}",width=290,height=100,font=("opensans",15))
        
        self.motd_label.place(x=140,y=20)

        self.mods_label = ctk.CTkTextbox(self.big_frame_2,width=474,font=("opensans",20))
        self.mods_label.place(x=10,y=140)
        self.player_label = ctk.CTkTextbox(self.big_frame,width=380,height=400,font=("opensans",20))
        self.player_label.place(x=10,y=25)
        self.plugins_label = ctk.CTkTextbox(self.big_frame_2,width=474,height=138,font=("opensans",20))
        self.plugins_label.place(x=10,y=354)

        self.player_info = ctk.CTkLabel(self.big_frame,text="shows a max of 12 players.",text_color="grey",
        font=("opensans",15))
        self.player_info.place(x=20,y=450)
            
        self.placeholder_frame = ctk.CTkFrame(self.window,width=1000,corner_radius=10,fg_color="transparent")
        self.placeholder_frame.place(x=300,y=230)
        placeholder_image = ctk.CTkImage(Image.open("assets/404.png"),size=(200,200))
        self.placeholder_label = ctk.CTkLabel(self.placeholder_frame,text="",image=placeholder_image,)
        self.placeholder_label.place(x=0,y=30)
        self.placeholder_text = ctk.CTkLabel(self.placeholder_frame,text="Nothing here yet.",font=("opensans",50))
        self.placeholder_text.pack(pady=200,side= TOP )
        
        # -- creating tags for color
        self.mods_label.tag_config("warning_tag",foreground=nord["nord11"])
        self.player_label.tag_config("warning_tag",foreground=nord["nord11"])
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
        self.suchen_btn.configure(fg_color=nord["nord1"],hover_color=nord["nord2"])

        
    def getIcon(self,icon,icon_name):
        try:
            icon_data = base64.b64decode(icon.split(",")[1])
            image_icon = ctk.CTkImage(Image.open(io.BytesIO(icon_data)),size=(100,100))
            self.icon_status = True
            return image_icon,self.icon_status
        except Exception :
            CTkMessagebox.CTkMessagebox(self.window,
            message="Icon not found",icon="warning",title="Icon",font=("opensans",15))
            print("DEBUG: Wenn Icon 'None' ist kann dieser fehler kommen",)
            image_icon = ctk.CTkImage(Image.open("assets/question-sign.png"),size=(100,100))
            self.icon_status = False
            return image_icon,self.icon_status
    def widget_animation(self):
        self.frame_x -= 10
        if self.frame_x >= 15:
            self.big_frame_2.place(x=self.frame_x,y=180)
            self.window.after(1,self.widget_animation)

        self.frame_x_2 -= 10
        if self.frame_x_2 >= 580:
            self.big_frame.place(x=self.frame_x_2,y=180)
            self.window.after(100,self.widget_animation)

    def getEingabe(self,):
        self.widget_animation()

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
            self.motd_label.configure(text=self.motd)

            # -- löschen von vorherigen eingaben
            self.mods_label.delete(1.0,tk.END)
            self.player_label.delete(1.0,tk.END)
            self.plugins_label.delete(1.0,tk.END)
            # --
            if self.mods != "":
                self.mods_label.insert(1.0,f"""Mods List:\n
{self.mods}""")
            else:
                self.mods_label.insert(1.0,"""
I wasn't able to obtain this information.""","warning_tag")
                self.mods_label.insert(1.0,"Mods List:\n ")


            image_icon,self.icon_status = self.getIcon(self.server_icon,self.icon_status)
            self.icon.configure(image=image_icon,)
            if not self.icon_status:
                self.tooltip_1.configure(message="Icon not found")
            else:
                self.tooltip_1.configure(message=f"Server icon from: {self.host} ")
            
            if self.player_list != "":
                self.player_label.insert(1.0,f"""Player List:\n
{self.player_list}

                """)
            else:
                self.player_label.insert(1.0,"""
I wasn't able to obtain this information.""","warning_tag")
                self.player_label.insert(1.0,"Player List:\n")
            if self.plugins != "":
            
                self.plugins_label.insert(1.0,f"""Plugins List:\n
{self.plugins}
            """)
            else:
                self.plugins_label.insert(1.0,"""
I wasn't able to obtain this information.""","warning_tag")
                self.plugins_label.insert(1.0,"Plugins List:\n")

            # -- Textbox deaktivieren nach einfügen
            self.mods_label.configure(state="disabled")
            self.player_label.configure(state="disabled")
            self.plugins_label.configure(state="disabled")

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



            self.motd_label.configure(bg_color=eerie_black)
            self.eingabe_feld.delete(0,tk.END)

        except Exception as e:
            CTkMessagebox.CTkMessagebox(self.window,message="This Server does not exist",
            icon="warning",title="Invalid Server Name",font=("opensans",15))
            self.eingabe_feld.delete(0,tk.END)
            print(e)
