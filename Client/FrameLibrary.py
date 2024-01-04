import tkinter
import customtkinter
from customtkinter import *


class RegisterFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        self.tabview = CTkTabview(master=self)
        self.tabview.grid(row=0, column=2, sticky="nsew")
        self.tabview.pack(padx=20, pady=20)

        self.tabview.add('Register')
        self.tabview.add('Login')

        self.login_username = customtkinter.CTkTextbox(self.tabview.tab('Login'))
        self.login_username.grid(row=1, column=0, padx=(40, 0), pady=(20, 20))

        self.login_password = customtkinter.CTkTextbox(self.tabview.tab('Login'))
        self.login_password.grid(row=2, column=0, padx=(40, 0), pady=(40, 20))

        self.login_enter = customtkinter.CTkButton(self.tabview.tab('Login'))
        self.login_enter.grid(row=3, column=0, padx=(40, 0), pady=(20, 20))

