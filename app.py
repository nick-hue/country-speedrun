import controller
from tkinter import *
import customtkinter as ctk
import time

# FONTS
TIMER_FONT = ("Open Sans", 30)
BUTTON_FONT = ("Open Sans", 20, 'bold')
LETTER_LABEL_FONT = ("Open Sans", 20)
ENTRY_FONT = ("Open Sans", 18)
ENTRY_FONT_WIN =  ("Open Sans", 18, 'bold')

# WIDGET DIMENSIONS
BUTTON_HEIGHT = 18
BUTTON_WIDTH = 90

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Country Speedrun")
        self.resizable(False, False)
        
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.countries = controller.get_countries()
        self.alphabet_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "Y", "Z"] # not W, X 
        self.correct_entries = 0

        # FRAMES 
        self.timer_frame = ctk.CTkFrame(self, corner_radius=0)
        self.timer_frame.grid(row=0, column=0, sticky = "ew")

        self.countries_frame = ctk.CTkFrame(self, corner_radius=0)
        self.countries_frame.grid(row=1, column=0, sticky = "ew")

        # TIMER FRAME WIDGETS

        self.timer_label = ctk.CTkLabel(self.timer_frame, text="00:00", font=TIMER_FONT)
        self.timer_label.grid(row=0, column=0, padx = 10, pady = 10)
        print(self.timer_label.cget("text_color"))

        self.start_button = ctk.CTkButton(self.timer_frame, text="Start", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, font=BUTTON_FONT, command=self.start_timer)
        self.start_button.grid(row=0, column=1, padx = 10, pady = 10)

        self.stop_button = ctk.CTkButton(self.timer_frame, text="Stop", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, font=BUTTON_FONT, command=self.stop_timer)
        self.stop_button.grid(row=0, column=2, padx = 10, pady = 10)

        self.reset_buton = ctk.CTkButton(self.timer_frame, text="Reset", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, font=BUTTON_FONT, command=self.reset_timer)
        self.reset_buton.grid(row=0, column=3, padx = 10, pady = 10)

        ctk.CTkLabel(self.timer_frame, text="No country starts with the letter 'X' or 'W'", text_color="red").grid(row=0, column=4, padx = 80, pady = 10)

        # COUNTRIES FRAME WIDGETS
        self.entries=[]
        self.cell_values=[]

        current_row=-1

        for idx, letter in enumerate(self.alphabet_letters):
            if idx%6==0:
                current_row+=1

            text = StringVar()
            text.trace_add('write', lambda name, index, mode, idx=idx, letter=letter: self.on_type(idx, letter))
            self.cell_values.append(text)       
            
            ctk.CTkLabel(self.countries_frame, text=f"{letter}:", font=LETTER_LABEL_FONT).grid(row=current_row,column=2*(idx%6), padx=6, pady=5)
            entry = ctk.CTkEntry(self.countries_frame, textvariable=text, state=DISABLED, font=ENTRY_FONT)
            entry.grid(row=current_row,column=2*(idx%6)+1)
            self.entries.append(entry)

        # TIMER VARIABLES
        self.running = False
        self.start_time = 0
        self.elapsed_time_before_stop = 0   

    def on_type(self, *args):
        print(f"Traced")
        print(args)

        guess = self.entries[int(args[0])].get()
        filtered_countries = [country for country in self.countries if country.startswith(args[1].lower())]

        if guess.lower() in filtered_countries:
            self.entries[int(args[0])].configure(state=DISABLED, text_color = "green", font=ENTRY_FONT_WIN)
            self.correct_entries+=1

        if self.correct_entries == 3:
            self.exit_game()

    def exit_game(self):
        print(f"Congratulations...\nyour time was: {self.timer_label.cget('text')}")   
        self.running = False    

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = int(time.time()) - self.elapsed_time_before_stop
            self.update_timer()

            for entry in self.entries:
                entry.configure(state=NORMAL)

    def stop_timer(self):
        if self.running:
            self.running = False
            self.elapsed_time_before_stop = int(time.time()) - self.start_time

            for entry in self.entries:
                entry.configure(state=DISABLED)

    def reset_timer(self):
        self.running = False
        self.timer_label.configure(text="00:00")
        self.elapsed_time_before_stop = 0

        for entry in self.entries:
            entry.configure(state=NORMAL)
            entry.delete(0, END)
            entry.configure(state=DISABLED, text_color="#DCE4EE")
            
    def update_timer(self):
        if self.running:
            elapsed_time = int(time.time()) - self.start_time
            minutes, seconds = divmod(elapsed_time, 60)
            time_str = f"{minutes:02}:{seconds:02}"
            self.timer_label.configure(text=time_str)
            self.after(1000, self.update_timer)

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()

