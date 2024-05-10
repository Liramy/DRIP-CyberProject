import os
import tkinter

import customtkinter
from tkinter import ttk
from tkinter import *
import joblib

from PIL import Image, ImageTk
import pickle

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self, sock):
        super().__init__()

        self.socket = sock
        self.title("ClearView.py")
        self.geometry("700x450")
        self.subject_list = ["subject"]
        self.link_list = {"subject":[""]}

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Assets")
        
        text_font = customtkinter.CTkFont(family="Segoe UI", size=15)
        label_font = customtkinter.CTkFont(family="Segoe UI", size=30, weight="bold")
        entry_font = customtkinter.CTkFont(family="Segoe UI", size=20)
        
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "logo-no-background.png")), 
                                                 dark_image=Image.open(os.path.join(image_path, "logo-white-no-background.png")),
                                                 size=(100, 100))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.search_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "search-dark.png")),
                                                     light_image=Image.open(os.path.join(image_path, "search-light.png")), size=(25, 25))

        self.search_image_button = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "search-dark.png")),
                                                     light_image=Image.open(os.path.join(image_path, "search-light.png")), size=(75, 75))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Full View", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=" Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", 
                                                   command=self.home_button_event, font=text_font)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.search_frame_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, 
                                                      text="Search", fg_color="transparent", text_color=("gray10", "gray90"), 
                                                      hover_color=("gray70", "gray30"), font=text_font,
                                                      image=self.search_image, anchor="w", command=self.search_frame_button_event)
        self.search_frame_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event, fg_color=("gray60", "#26272E"),
                                                                button_color=("gray50","#222227"), button_hover_color=("#4F5263","#4F5263"))
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="Your library", 
                                                                   font=label_font)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.library_select = customtkinter.CTkOptionMenu(self.home_frame, values=self.subject_list,
                                                                command=self.change_subject, fg_color=("gray60", "#26272E"),
                                                                button_color=("gray50","#222227"), button_hover_color=("#4F5263","#4F5263"))
        self.library_select.grid(row=1, column=0, padx=10, pady=10)
        
        self.library_text = customtkinter.CTkTextbox(self.home_frame, width=220, height=300)
        self.library_text.grid(row=1, rowspan=2, column=1, padx=10, pady=10)
        self.library_text.configure(state="disabled")

        # create second frame
        self.search_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_rowconfigure(3, weight=1)

        self.search_bar = customtkinter.CTkEntry(self.search_frame, width=400, height=50, justify="center",
                                                 font=entry_font, placeholder_text="Search subject")
        self.search_bar.grid(row=0, column=0, padx=20, pady=20)
        
        self.search_date = customtkinter.CTkEntry(self.search_frame, width=250, height=40,
                                                  placeholder_text="Enter date: 3d, 4m, 6y", font=entry_font,
                                                  justify="center")
        self.search_date.grid(row=1, column=0, padx=20, pady=20)
        
        self.search_button = customtkinter.CTkButton(self.search_frame, width=100, height=100,
                                                     fg_color="transparent", hover_color=("#4F5263","#4F5263"),
                                                     image=self.search_image_button, text="",
                                                     command=self.search_subject)
        self.search_button.grid(row=2, column=0, padx=20, pady=20)
        
        self.search_label = customtkinter.CTkLabel(self.search_frame, text=
                                                   "Search the subject you wish to learn more about.\n" + 
                                                   'For example: "The movie `Kung Fu Panda`"\n' +
                                                   'Another: "The science behind nueral network"', font=entry_font, 
                                                   width=400, height=400, wraplength=400)
        self.search_label.grid(row=3, column=0,padx=20, pady=0)
        
        self.load_subjects()

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.search_frame_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "search":
            self.search_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.search_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def search_frame_button_event(self):
        self.select_frame_by_name("search")
        
    def change_subject(self, new_subject):
        self.library_text.configure(state="normal")
        self.library_text.delete("0.0", "end")
        
        a = self.link_list[new_subject]
        lines = []
        if len(a) > 0:
            for line in a:
                lines.append(f"{line[0]}. \nPropaganda precent: {round(line[1], 3)*100}%")
            text = '\n\n'.join(lines)
        else: 
            text = "No results found"
        
        self.library_text.insert("0.0", text=text)

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def search_subject(self):
        subject = self.search_bar.get()
        if len(subject) < 4:
            return
        
        allowed_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-1234567890 "
        if not all(char in allowed_characters for char in subject):
            return
        
        date = self.search_date.get()
        data = pickle.dumps({"Search":(subject, date)})
        self.socket.send(data)

        raw_results = self.socket.recv(16384)
        data = pickle.loads(raw_results)
        
        self.subject_list.append(subject)
        self.link_list[subject] = data
        
        self.save_subject()
        
        self.library_select.destroy()
        self.library_select = customtkinter.CTkOptionMenu(self.home_frame, values=self.subject_list,
                                                                command=self.change_subject, fg_color=("gray60", "#26272E"),
                                                                button_color=("gray50","#222227"), button_hover_color=("#4F5263","#4F5263"))
        self.library_select.grid(row=1, column=0, padx=10, pady=10)
        
    def save_subject(self):
        joblib.dump(self.link_list, "SavedData.fv")
        joblib.dump(self.subject_list, "SavedSubjectData.fv")
        
    def load_subjects(self):
        try:
            self.link_list = joblib.load("SavedData.fv")
            self.subject_list = joblib.load("SavedSubjectData.fv")
        except Exception as e:
            self.link_list = {}
            self.subject_list = ["Subject"]
        finally:
            self.library_select.destroy()
            self.library_select = customtkinter.CTkOptionMenu(self.home_frame, values=self.subject_list,
                                                                    command=self.change_subject, fg_color=("gray60", "#26272E"),
                                                                    button_color=("gray50","#222227"), button_hover_color=("#4F5263","#4F5263"))
            self.library_select.grid(row=1, column=0, padx=10, pady=10)
        
        