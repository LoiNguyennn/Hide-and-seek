import tkinter as tk
from tkinter import filedialog, ttk
import os

class GameMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File and Level Selector")
        self.level = 0
        self.file_name = ""
        self.create_widgets()
        self.run_menu()

    def create_widgets(self):
        self.title('Hide And Seek')
        self.geometry('420x270+600+250')
        self.resizable(width=False, height=False)
        # Frame for the entry box and its label
        self.main_lable = tk.Label(text = "\nGAME MENU\n", fg = ('#%02x%02x%02x' % (168, 208, 141)), font=("Helvetica", 16, "bold"))
        self.main_lable.pack()
        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(fill=tk.X)
        # Label for the entry box
        self.input_label = tk.Label(self.entry_frame, text=" Input maps:     ", font=("Helvetica", 10))
        self.input_label.pack(side=tk.LEFT)

        # Create an entry box for file name display and input
        self.file_name_entry = tk.Entry(self.entry_frame, width=41)
        self.file_name_entry.insert(0, "file's directory path")
        self.file_name_entry.pack(side=tk.LEFT, padx=5)
        
        self.space_label = tk.Label(text = "\n")
        self.space_label.pack()
        # Create a button to browse for files
        self.browse_button = tk.Button(self.entry_frame, text="Browse", command=self.browse_file, width = 7, bg = ('#%02x%02x%02x' % (200, 200, 200)))
        self.browse_button.pack(side=tk.LEFT)

        # Frame for the file and level selection comboboxes and their labels
        self.selection_frame = tk.Frame(self)
        self.selection_frame.pack(fill=tk.X)

        self.space_label1 = tk.Label(text = "\n")
        self.space_label1.pack()
        
        # Label for the file selection combobox
        self.file_label = tk.Label(self.selection_frame, text="Available maps:", width=12, font=("Helvetica", 10))
        self.file_label.pack(side=tk.LEFT)

        # Create a combobox for file selection
        self.file_combobox = ttk.Combobox(self.selection_frame, width=22)
        self.file_combobox.bind('<<ComboboxSelected>>', self.update_entry_from_combobox)
        self.file_combobox.pack(side=tk.LEFT, padx=(0, 20))

        # Label for the level selection combobox
        self.level_label = tk.Label(self.selection_frame, text="Choose level:", width=10, font=("Helvetica", 10))
        self.level_label.pack(side=tk.LEFT)

        # Create a combobox for level selection
        self.level_combobox = ttk.Combobox(self.selection_frame, values=["1", "2", "3", "4"], state="readonly", width=5)
        self.level_combobox.pack(side=tk.LEFT)

        # Create an enter button to submit the selections
        self.enter_button = tk.Button(self, text="Enter", command=self.submit, width = 10, font=("Helvetica", 10, "bold"), bg = ('#%02x%02x%02x' % (200, 200, 200)))
        self.enter_button.pack()

        self.message_label = tk.Label(self, text="", fg="red")
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


    # Function to submit the selected file name and level
    def submit(self):
        selected_file_name = self.file_name_entry.get()
        selected_level = self.level_combobox.get()
        foul = 0
        message = ""
        if not selected_level:
            message += "You haven't chosen a level!\n"
            foul += 1
        if self.check_file(selected_file_name):
            message += "You chose the wrong directory path, please enter again.\n"
            foul += 1
        if foul == 0:
            self.file_name = selected_file_name
            self.level = selected_level
            self.destroy()
        else:
            self.message_label.config(text=message)

    def run_menu(self):
        self.mainloop()
