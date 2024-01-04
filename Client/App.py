import tkinter

import customtkinter
from tkinter import ttk
from tkinter import *
import FrameLibrary

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title("DRIP")
        self.geometry(f"{1100}x{580}")

        self.frames = [FrameLibrary.RegisterFrame(self)]
        self.frames[0].pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()