import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.font as tkFont
import os

class GameMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File and Level Selector")
        self.level = None
        self.file_name = None
        self.exit = False
        self.create_widgets()
        self.run_menu()
    
    def create_widgets(self):
        self.title('Hide And Seek')
        self.geometry('570x350+600+250')
        self.resizable(width=False, height=False)
        # Frame to hold the label and button
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Exit button (NÊN ĐẶT Ở ĐÂU)-------------------------------
        # self.exit_button = tk.Button(top_frame, text="Exit", command=self.exitGame, width=5, font=("Helvetica", 10, "bold"), bg=('#%02x%02x%02x' % (200, 200, 200)))
        # self.exit_button.pack(side=tk.LEFT)
        element_font = tkFont.Font(family="Helvetica", size=11)
        main_font = tkFont.Font(family="Helvetica", size = 12, weight= 'bold')
        # Main label
        self.main_label = tk.Label(top_frame, text="\nGAME MENU\n", fg=('#%02x%02x%02x' % (168, 208, 141)), font=("Helvetica", 22, "bold"))
        self.main_label.pack(side=tk.LEFT, padx=180)
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(fill=tk.X)
        
        # Label for the entry box
        self.input_label = tk.Label(self.entry_frame, text=" Input map:          ", width=15, font= main_font, fg = ('#%02x%02x%02x' % (168, 208, 141)))
        self.input_label.pack(side=tk.LEFT)

        # Create an entry box for file name display and input
        self.file_name_entry = tk.Entry(self.entry_frame, width=37, font = element_font)
        self.file_name_entry.insert(0, "  file's directory path")
        self.file_name_entry.pack(side=tk.LEFT, ipadx=15)

        #Space
        self.space_label = tk.Label(text = "\n")
        self.space_label.pack()

        # Create a button to browse for files
        self.browse_button = tk.Button(self.entry_frame, text="Browse", command=self.browse_file, width = 7, font = ("Helvetica", 10, 'bold'), bg = ('#%02x%02x%02x' % (200, 200, 200)))
        self.browse_button.pack(side=tk.LEFT)

        # Frame for the file and level selection comboboxes and their labels
        self.selection_frame = tk.Frame(self)
        self.selection_frame.pack(fill=tk.X)

        self.space_label1 = tk.Label(text = "\n")
        self.space_label1.pack()
        
        # Label for the file selection combobox
        self.file_label = tk.Label(self.selection_frame, text=" Available maps:", width=14, font= main_font, fg = ('#%02x%02x%02x' % (168, 208, 141)))
        self.file_label.pack(side=tk.LEFT)

        # Create a combobox for file selection
        self.file_combobox = ttk.Combobox(self.selection_frame, width=8, font = element_font)
        self.file_combobox.bind('<<ComboboxSelected>>', self.update_entry_from_combobox)
        self.file_combobox.pack(side=tk.LEFT, padx=(5, 20))

        # Label for the level selection combobox
        self.level_label = tk.Label(self.selection_frame, text="Choose level:", width=10, font= main_font, fg = ('#%02x%02x%02x' % (168, 208, 141)))
        self.level_label.pack(side=tk.LEFT)

        # Create a combobox for level selection
        self.level_combobox = ttk.Combobox(self.selection_frame, values=["1", "2", "3", "4"], state="readonly", width=3)
        self.level_combobox.pack(side=tk.LEFT, padx=(5, 20))

        # Label for the speed box entry box
        self.level_label = tk.Label(self.selection_frame, text="Speed:", width=6, font= main_font, fg = ('#%02x%02x%02x' % (168, 208, 141)))
        self.level_label.pack(side=tk.LEFT)

        # Create a combobox for level selection
        vcmd = (self.register(self.on_validate), '%P')
        self.speed_entry = ttk.Entry(self.selection_frame, validate="key", validatecommand=vcmd, width = 5, font = element_font)
        self.speed_entry.insert(0, "2")
        self.speed_entry.pack(side=tk.LEFT)
        
        #Increase/Decrease buttons
        self.pixel = tk.PhotoImage(width=10, height=100)  # Create a transparent image
        buttons_frame = tk.Frame(self.selection_frame)
        self.inc_button = tk.Button(buttons_frame, text='+', font = ("Helvetica", 10,'bold'), image=self.pixel, width=10, height=5, compound=tk.CENTER, command=self.increment)
        self.inc_button.pack(side=tk.TOP, fill=tk.X)
        self.dec_button = tk.Button(buttons_frame, text='-', font = ("Helvetica", 18), image=self.pixel, width=10, height=5, compound=tk.CENTER, command=self.decrement)
        self.dec_button.pack(side=tk.BOTTOM, fill=tk.X)
        buttons_frame.pack(side=tk.LEFT)


        # Create an enter button to submit the selections
        self.enter_button = tk.Button(self, text="Enter", command=self.submit, width = 10, font=("Helvetica", 10, "bold"), bg = ('#%02x%02x%02x' % (200, 200, 200)))
        self.enter_button.pack()
        
        self.message_label = tk.Label(self, text="", fg="red", font = element_font)
        self.message_label.pack()

        # Initialize the file combobox
        self.update_file_combobox('map')

    def update_file_combobox(self, initial_dir):
        files = self.read_files(initial_dir)
        self.file_combobox['values'] = files

    def read_files(self, initial_dir):
        list_file = []
        for root, dirs, files in os.walk(initial_dir):
            for file in files:
                if file.endswith('.txt'):
                    list_file.append(file[:-4])
        return list_file

    # Function to update the entry box with the selected file name from the combobox
    def update_entry_from_combobox(self, event):
        selected_file = self.file_combobox.get()
        self.file_name_entry.delete(0, tk.END)
        self.file_name_entry.insert(0, selected_file)

    # Function to browse for a file and update the entry box with the file path
    def browse_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            self.file_name_entry.delete(0, tk.END)
            self.file_name_entry.insert(0, filepath)

    def is_number(self, char):
        return char.isdigit()

    def on_validate(self, P):
        if P == "" or P.isdigit():
            return True
        else:
            return False

    def check_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                return False
        except FileNotFoundError:
            try:
                with open('map/' + file_name + '.txt', 'r') as file:
                    return False
            except FileNotFoundError:
                return True
    #Exit from menu
    def exitGame(self):
        self.exit = True
        self.destroy()
    # Function to submit the selected file name and level
    def submit(self):
        selected_file_name = self.file_name_entry.get()
        selected_level = self.level_combobox.get()
        selected_speed = self.speed_entry.get()
        foul = 0
        message = "\n"
        
        # Check if a level is selected
        if not selected_level:
            message += "You haven't chosen any level!\n"
            foul += 1
        if selected_level == '4':
            message += "This level isn't available yet!\n"
            foul += 1
        # Check if the file name is not 'map' and the file exists
        if selected_file_name == 'map' or self.check_file(selected_file_name):
            message += "You choose the wrong directory path, please enter again.\n"
            foul += 1
        
        # Check if the speed entry is a number and within an acceptable range
        try:
            speed = int(selected_speed)
            if speed < 1 or speed > 10:  # Assuming the speed range is 1 to 5
                message += "Speed must be a number between 1 and 10.\n"
                foul += 1
        except ValueError:
            message += "Speed must be a number.\n"
            foul += 1
        
        # If no errors, proceed with setting the values and destroying the window
        if foul == 0:
            self.file_name = selected_file_name
            self.level = int(selected_level)
            self.speed = speed  # Save the speed value
            self.destroy()
        else:
            self.message_label.config(text=message)
    
    def increment(self):
        try:
            current_value = int(self.speed_entry.get())
            if current_value == 9:
                return
            self.speed_entry.delete(0, tk.END)
            self.speed_entry.insert(0, str(current_value + 1))
        except ValueError:
            self.speed_entry.delete(0, tk.END)
            self.speed_entry.insert(0, '0')

    def decrement(self):
        try:
            current_value = int(self.speed_entry.get())
            if current_value == 1:
                return
            self.speed_entry.delete(0, tk.END)
            self.speed_entry.insert(0, str(current_value - 1))
        except ValueError:
            self.speed_entry.delete(0, tk.END)
            self.speed_entry.insert(0, '0')

    def run_menu(self):
        self.mainloop()



class EndMenu(tk.Tk):
    def __init__(self, win, point):
        super().__init__()
        self.win = win
        self.goBack = True
        self.point = point
        self.create_widget()
        self.run_menu() 
    def create_widget(self):
        self.title('Hide And Seek')
        self.geometry('250x170+600+250')
        self.resizable(width=False, height=False)
        element_font = tkFont.Font(family="Helvetica", size=12)
        # Styling
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), background='#c8c8c8')

        # Result label
        if self.win:
            message_label = "Win"
        else:
            message_label = "Lose"
        self.m_label = ttk.Label(self, text=f"Result: {message_label}", font = element_font)
        self.m_label.pack(pady=5)

        # Points label
        self.p_label = ttk.Label(self, text=f"Score: {self.point}", font = element_font)
        self.p_label.pack(pady=5)

        # Frame for buttons
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(fill=tk.X, padx=10, pady=10)

        # Replay button
        self.replay_button = tk.Button(self.entry_frame, text="Replay", font=("Helvetica", 10, "bold"), command=self.rePlay, width=20)
        self.replay_button.pack(side=tk.TOP)

        # Go back to menu button
        self.menu_button = tk.Button(self.entry_frame, text="Go back to menu", font=("Helvetica", 10, "bold"), command = self.goBackToMainMenu, width=20)
        self.menu_button.pack()

    def goBackToMainMenu(self):
        self.goBack = True
        self.destroy()

    def rePlay(self):
        self.goBack = False
        self.destroy()

    def run_menu(self):
        self.mainloop()
