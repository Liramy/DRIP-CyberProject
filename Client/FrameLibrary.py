import tkinter
import customtkinter
from customtkinter import *
import AppLib.Validations


class RegisterFrame(CTkTabview):
    def __init__(self, master,  **kwargs):
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
            self.tab('Login'), width=200, height=50, text="Log In", font=("Segoe", 25), command=self.__loginCommand)
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
        
    def __loginCommand(self):
        username = self.login_username.get()
        valid_username = self.validate_username(username)

        password = self.login_password.get()
        valid_password = self.validate_password(password)

        
        
    def validate_username(self, username:str, minimumUsernameLength  = 4, maximumUsernameLength = 16):
        
        # Check if length is between constant numbers
        if len(username) > maximumUsernameLength or len(username) < minimumUsernameLength:
            return False
        
        # Check for no special symbols
        character_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
                        'r', 's', 't', 'u', 'v', 'w','x','y','A','B','C','D','E','F','G','H','I','J','K','L',
                        'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', '0', '1', '2', '3', '4', '5',
                        '6', '7', '8', '9']
        user_copy = username
        for i in character_list:
            user_copy = user_copy.replace(i, '')
        
        return len(user_copy) == 0

    def validate_password(self, password:str, minimumPasswordLength = 8, maximumPasswordLength = 18):
        # Check if length is between constant numbers
        if len(password) > maximumPasswordLength or len(password) < minimumPasswordLength:
            return False
        
        # Check for no special symbols
        character_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
                        'r', 's', 't', 'u', 'v', 'w','x','y','A','B','C','D','E','F','G','H','I','J','K','L',
                        'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z', '0', '1', '2', '3', '4', '5',
                        '6', '7', '8', '9', '-','_','$','%']
        password_copy = password
        for i in character_list:
            password_copy = password_copy.replace(i, '')
        
        return len(password_copy) == 0
