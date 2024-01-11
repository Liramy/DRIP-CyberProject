import tkinter
import customtkinter
from customtkinter import *


class RegisterFrame(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Login")
        self.add("Register")

        self.login_label = customtkinter.CTkLabel(
            master=self.tab("Login"), font=("Segoe", 30), text="Enter Username")
        self.login_label.grid(row=1, column=1, padx=(20,20))
        self.login_label.place(relx=0.3, rely=0.1, anchor=CENTER)

        self.login_username = customtkinter.CTkEntry(
            self.tab('Login'), justify='center' ,width=400, height=60, font=("Segoe", 30))
        self.login_username.grid(row=1, column=2, sticky="nsew", pady=(20, 20), padx=(20,20))
        self.login_username.place(relx=0.65, rely=0.1, anchor=CENTER)

        self.password_label = customtkinter.CTkLabel(
            master=self.tab("Login"), font=("Segoe", 30), text="Enter Password")
        self.password_label.grid(row=2, column=1, padx=(20,20))
        self.password_label.place(relx=0.3, rely=0.3, anchor=CENTER)

        self.login_password = customtkinter.CTkEntry(
            self.tab('Login'), width=400, height=60, font=("Segoe", 30), show='*', justify='center')
        self.login_password.grid(row=2, column=2, pady=(20, 20))
        self.login_password.place(relx=0.65, rely=0.3, anchor=CENTER)

        self.login_enter = customtkinter.CTkButton(
            self.tab('Login'), width=200, height=50, text="Log In", font=("Segoe", 25))
        self.login_enter.place(relx=0.5, rely=0.5, anchor=CENTER)

        #--------------------------------------------------------------------------

        self.register_label = customtkinter.CTkLabel(
            master=self.tab("Register"), font=("Segoe", 30), text="Enter Username")
        self.register_label.grid(row=1, column=1, padx=(20,20))
        self.register_label.place(relx=0.3, rely=0.1, anchor=CENTER)

        self.register_username = customtkinter.CTkEntry(
            self.tab('Register'), justify='center' ,width=400, height=60, font=("Segoe", 30))
        self.register_username.grid(row=1, column=2, sticky="nsew", pady=(20, 20), padx=(20,20))
        self.register_username.place(relx=0.65, rely=0.1, anchor=CENTER)

        self.password_register_label = customtkinter.CTkLabel(
            master=self.tab("Register"), font=("Segoe", 30), text="Enter Password")
        self.password_register_label.grid(row=2, column=1, padx=(20,20))
        self.password_register_label.place(relx=0.3, rely=0.3, anchor=CENTER)

        self.register_password = customtkinter.CTkEntry(
            self.tab('Register'), width=400, height=60, font=("Segoe", 30), show='*', justify='center')
        self.register_password.grid(row=2, column=2, pady=(20, 20))
        self.register_password.place(relx=0.65, rely=0.3, anchor=CENTER)

        self.register_label = customtkinter.CTkLabel(
            master=self.tab("Register"), font=("Segoe", 30), text="Confirm Password")
        self.register_label.grid(row=2, column=1, padx=(20,20))
        self.register_label.place(relx=0.3, rely=0.5, anchor=CENTER)

        self.register_register = customtkinter.CTkEntry(
            self.tab('Register'), width=400, height=60, font=("Segoe", 30), show='*', justify='center')
        self.register_register.grid(row=2, column=2, pady=(20, 20))
        self.register_register.place(relx=0.65, rely=0.5, anchor=CENTER)

        self.register_enter = customtkinter.CTkButton(
            self.tab('Register'), width=200, height=50, text="Register", font=("Segoe", 25))
        self.register_enter.place(relx=0.5, rely=0.7, anchor=CENTER)
