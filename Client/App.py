import socket
import tkinter

import customtkinter
from tkinter import ttk
from tkinter import *
import FrameLibrary
import torch

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        serverIP = '127.0.0.1'
        ServerPORT = 8202

        sock = socket.socket()
        #sock.connect((serverIP, ServerPORT))

        self.title("DRIP")
        self.geometry(f"{1100}x{580}")

        self.frames = [FrameLibrary.RegisterFrame(self, width=1000, height = 800)]
        self.frames[0].pack()

        self.frames[0].lower()

        self.mode = customtkinter.CTkComboBox(
            self, values=["System", "Dark", "Light"], width=200, justify='center', font=("Segoe", 20),
            command=self.change_mode, state="readonly")
        self.mode.pack()
        self.mode.place(rely=0.1, relx=0.1, anchor=CENTER)

    def change_mode(self, new_mode:str):
        customtkinter.set_appearance_mode(new_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()