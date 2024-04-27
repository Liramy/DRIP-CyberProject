import os
import tkinter
from typing import Tuple

import customtkinter
from tkinter import ttk
from tkinter import *

from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Tabs(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Login")
        self.add("Register")
        
        self.tab("Login").grid_columnconfigure(0, weight=1)
        self.tab("Register").grid_columnconfigure(0, weight=1)

        # add widgets on tabs
        label_font = customtkinter.CTkFont(family="Segoe UI", size=30)
        self.label = customtkinter.CTkLabel(
            master=self.tab("Login"), 
            height=30, width=100, 
            font=label_font, text="Log in", 
            text_color=("#26272E", "#E9EFE7"))
        self.label.grid(row=0, column=0, padx=0, pady=10)
        
        input_font = customtkinter.CTkFont(family="Segoe UI", size=15)
        self.username_login = customtkinter.CTkEntry(self.tab("Login"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Enter Username")
        self.username_login.grid(row=1, column=0, padx=0, pady=10)
        
        self.password_login = customtkinter.CTkEntry(self.tab("Login"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Enter Password", show="*")
        self.password_login.grid(row=2, column=0, padx=0, pady=10)
        
        self.login_button = customtkinter.CTkButton(self.tab("Login"), width=200, height= 75,
                                                    font=label_font, fg_color=("#C8CEC6", "#1E2025"),
                                                    corner_radius=20, text="Log In", command=self.log_in)
        
        self.login_button.grid(row=3, column=0, padx=0, pady=50)
        
        #---------------------------------------------------------------#
        # Register Page:
        self.label = customtkinter.CTkLabel(
            master=self.tab("Register"), 
            height=30, width=100, 
            font=label_font, text="Register", 
            text_color=("#26272E", "#E9EFE7"))
        self.label.grid(row=0, column=0, padx=0, pady=10)
        
        self.username_register = customtkinter.CTkEntry(self.tab("Register"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Enter Username")
        self.username_register.grid(row=1, column=0, padx=0, pady=10)
        
        self.password_register = customtkinter.CTkEntry(self.tab("Register"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Enter Password", show="*")
        self.password_register.grid(row=2, column=0, padx=0, pady=10)
        
        self.password_confirm = customtkinter.CTkEntry(self.tab("Register"), 
                                                       width=300, height= 20, font=input_font,
                                                       placeholder_text="Confirm Password", show="*")
        
        self.password_confirm.grid(row=3, column=0, padx=0, pady=10)
        
        
        self.register_button = customtkinter.CTkButton(self.tab("Register"), width=200, height= 75,
                                                    font=label_font, fg_color=("#C8CEC6", "#1E2025"),
                                                    corner_radius=20, text="Register", command=self.register)
        
        self.register_button.grid(row=4, column=0, padx=0, pady=30)
        
    def log_in(self):
        username = self.username_login.get()
        password = self.password_login.get()
        print(f'Username: {username} \nPassword: {password}')
        
    def register(self):
        username = self.username_register.get()
        password = self.password_register.get()
        password_confirm = self.password_confirm.get()
        
        print(f'username: {username}\nPassword: {password}\nPassword Confirmation: {password_confirm}')
    

class LoginApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("ClearView Login")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.tabview = Tabs(
            master=self, height=400, width=400, 
            fg_color=("#E9EFE7", "#26272E"), segmented_button_selected_color=("#2A2C35", "#2A2C35"),
            segmented_button_selected_hover_color=("#4F5263","#4F5263"), corner_radius=20)
        self.tabview.grid(row=0, column=1, padx=20, pady=10)
        
app = LoginApp()
app.mainloop()