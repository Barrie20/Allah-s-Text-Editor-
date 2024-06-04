import PySimpleGUI as sg
import io
import os
from datetime import datetime

# Global Variables
current_size = 11
current_font = "Arial"
dark_mode = False
script_path = os.path.dirname(os.path.abspath(file))
filename = None
first_time_save = True
menu_font = ('Arial', 14)

# Function Definitions

def about():
    sg.popup(
        f"Alfa's Text Editor v1.0 Beta\nCopyright © {datetime.now().year}\nDeveloped by Alpha Yerroh Barrie",
        title="About",
        font=('Arial', 12),
    )

def open_file():
    global filename
    filename = sg.popup_get_file(
        "Open Text File",
        default_extension=".txt",
        file_types=(("Text Files", "*.txt"), ("All Files", "*.*")),
        initial_folder=script_path,
    )
    if filename:
        try:
            with io.open(filename, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            sg.popup_error(f"Error opening file: {e}")
    return ""

def save_file(data):
    global filename
    if filename:
        try:
            with io.open(filename, "w", encoding="utf-8") as f:
                f.write(data)
            sg.popup_notify("File Saved Successfully!")
        except Exception as e:
            sg.popup_error(f"Error saving file: {e}")
    else:
        save_as(data)

def save_as(data):
    global filename, first_time_save
    filename = sg.popup_get_file(
        "Save As",
        default_extension=".txt",
        save_as=True,
        file_types=(("Text Files", "*.txt"), ("All Files", "*.*")),
        initial_folder=script_path,
    )
    if filename:
        save_file(data)
        first_time_save = False

def word_count(text):
    words = text.split()
    return len(words)

def find_text(text, query):
    start = 0
    while True:
        start = text.find(query, start)
        if start == -1:
            return
        yield start, start + len(query)
        start += len(query) 

def change_case(text, case_type):
    if case_type == "Upper":
        return text.upper()
    elif case_type == "Lower":
        return text.lower()
    elif case_type == "Title":
        return text.title()
    else:
        return text 

def toggle_dark_mode(window):
    global dark_mode
    dark_mode = not dark_mode
    theme = "DarkAmber" if not dark_mode else "Black"
    sg.theme(theme)
    window.refresh()
    for key in window.key_dict:
        try:
            window[key].update(background_color=sg.theme_background_color(),
                               text_color=sg.theme_text_color())
        except:
            pass

# Theme 
sg.theme("DarkAmber")

# Menu and Layout
menu = [
    ["File", ["New", "Open", "Save", "Save As", "---", "Exit"]],
    ["Edit", ["Font", ["Arial", "Courier New", "Helvetica", "Times New Roman"],
              "Size", ["8", "11", "14", "18", "22"], "---", "Change Case", ["Upper", "Lower", "Title"]]],
    ["Tools", ["Word Count", "Find", "Replace"]],
    ["View", ["Dark Mode"]],
    ["About", ["Version"]],
]

layout = [
    [sg.Menu(menu, font=menu_font)],
    [sg.Multiline(key="_text_", expand_x=True, expand_y=True, font=(current_font, current_size))],
    [sg.StatusBar("Ready", key="_status_", size=(80, 1))],
]

# Main Program
window = sg.Window("Alfa's Text Editor", layout, resizable=True, finalize=True)
window.maximize()

text_element = window["_text_"]

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if event == "New":
        if values["_text_"] and (
            first_time_save or sg.popup_yes_no("Save changes before creating a new file?") == "Yes"
        ):
            save_file(values["_text_"])
        text_element.update("")
        filename = None
        first_time_save = True

    elif event == "Open":
        file_contents = open_file()
        if file_contents:
            text_element.update(file_contents)
            first_time_save = False

    elif event in ("Save", "Save As"):
        save_file(values["_text_"]) if event == "Save" else save_as(values["_text_"])
