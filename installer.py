import os
import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog
from urllib import request as urllib_request
from PIL import Image, ImageTk
import urllib

def download_and_save_file(url, filename):
    try:
        with urllib_request.urlopen(url) as response:
            with open(filename, 'wb') as out_file:
                out_file.write(response.read())
        return True
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas pobierania pliku: {e}")
        return False

def create_folder(folder_name):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return True
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas tworzenia folderu: {e}")
        return False

def save_background_color(color):
    with open("ustawienia.ini", "w") as f:
        f.write(f"KolorTla={color}")

def load_background_color():
    if os.path.exists("ustawienia.ini"):
        with open("ustawienia.ini", "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("KolorTla"):
                    return line.split("=")[1].strip()
    return "lime"

root = tk.Tk()
root.title("XAKE PACK | V1")
root.geometry("550x600")

bg_color = load_background_color()
root.config(bg=bg_color)

current_folder = os.path.dirname(__file__)
download_folder = os.path.join(current_folder, "downloads")
create_folder(download_folder)

def download_and_save_zip(url, filename):
    try:
        with urllib_request.urlopen(url) as response:
            with open(filename, 'wb') as out_file:
                out_file.write(response.read())
        messagebox.showinfo("Informacja", f"Plik {filename} został pobrany i zapisany.")
    except urllib.error.HTTPError as e:
        if e.code == 503:
            messagebox.showerror("Błąd", "Serwer jest niedostępny. Spróbuj ponownie później.")
        else:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas pobierania pliku: {e}")

ubrania = {
    "Koszulka Autora (KEYYQ MEMBERS)": "https://github.com/kejaaczek/dsfxakepack/raw/master/Koszulka%20Autora%20(KEYYQ%20MEMBERS).rar",
    "Koszulka Autora (XANNEK)": "https://github.com/kejaaczek/dsfxakepack/raw/master/Koszulka%20Autora%20(XANNEK).rar",
    "Koszulka Families (FUCK THE POLICE)": "https://github.com/kejaaczek/dsfxakepack/raw/master/Koszulka%20Families%20(FUCK%20THE%20POLICE).rar",
    "Koszulka Nike (NIKE BEST)": "https://github.com/kejaaczek/dsfxakepack/raw/master/Koszulka%20Nike%20(NIKE%20BEST).rar",
}

def install(nazwa, link, button):
    zip_filename = os.path.join(download_folder, f"{nazwa}.rar")
    download_and_save_zip(link, zip_filename)
    button.config(text="Pobrane", state="disabled")

buttons = []

for nazwa, link in ubrania.items():
    ubranie_frame = tk.Frame(root, bg="yellow", bd=2, relief=tk.RIDGE, borderwidth=4, padx=5, pady=5, highlightbackground="white", highlightthickness=2, highlightcolor="white", border="5")
    ubranie_frame.pack(pady=5, padx=5, fill=tk.X)
    tk.Label(ubranie_frame, text=nazwa, bg="yellow").pack(side=tk.LEFT)
    install_button = tk.Button(ubranie_frame, text="Zainstaluj", command=lambda nazwa=nazwa, link=link, button=None: install(nazwa, link, button), relief=tk.RAISED, borderwidth=1, padx=5, pady=5, bg="light blue", font=("Arial", 10, "bold"))
    install_button.pack(side=tk.RIGHT)
    buttons.append(install_button)


def open_settings():
    def choose_background_color():
        color = colorchooser.askcolor(title="Wybierz kolor tła")[1]
        if color:
            root.config(bg=color)
            save_background_color(color)

    def select_download_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            download_folder_var.set(folder_selected)

    settings_window = tk.Toplevel(root)
    settings_window.title("Ustawienia")
    settings_window.geometry("300x100")

    change_color_button = tk.Button(settings_window, text="Zmień kolor tła", command=choose_background_color)
    change_color_button.pack()

    download_folder_var = tk.StringVar()
    download_folder_var.set(download_folder)

    change_folder_button = tk.Button(settings_window, text="Zmień folder downloads", command=select_download_folder)
    change_folder_button.pack()

settings_button = tk.Button(root, text="Ustawienia", command=open_settings)
settings_button.pack()

root.mainloop()
