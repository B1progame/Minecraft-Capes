import curses
import os
import shutil
import json
import subprocess
import platform
from PIL import Image, ImageTk
import tkinter as tk


LANG_FILE = "language.json"
LANGUAGES = {
    "de": {
        "help": "↑↓ = Auswahl | Enter = Anwenden | v = Vorschau | l = Sprache | q = Beenden",
        "no_files": "Keine PNG-Dateien im 'images'-Ordner gefunden.",
        "title": "Vorschau"
    },
    "en": {
        "help": "↑↓ = Select | Enter = Apply | v = Preview | l = Language | q = Quit",
        "no_files": "No PNG files found in 'images' folder.",
        "title": "Preview"
    }
}



# === Config ===
SOURCE_DIR = "images"
STATE_FILE = "state.json"
CONFIG_FILE = "config.txt"

# === Helper-Functions ===
def load_language():
    if os.path.exists(LANG_FILE):
        try:
            with open(LANG_FILE, "r") as f:
                lang = json.load(f).get("lang", "en")
                return lang if lang in LANGUAGES else "en"
        except json.JSONDecodeError:
            return "en"
    return "en"

def save_language(lang):
    with open(LANG_FILE, "w") as f:
        json.dump({"lang": lang}, f)

def load_images():
    return [f for f in os.listdir(SOURCE_DIR) if f.endswith(".png")]

def format_image_name(filename, index):
    base = os.path.splitext(filename)[0]
    return f"R{index+1} {base}"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                return json.load(f).get("selected", None)
            except json.JSONDecodeError:
                return None
    return None

def save_state(selected):
    with open(STATE_FILE, "w") as f:
        json.dump({"selected": selected}, f)

def get_target_name():
    """
    Liest die erste Zeile aus CONFIG_FILE und gibt sie zurück.
    Falls CONFIG_FILE fehlt oder die erste Zeile fehlt/leer ist, wird ein Fehler ausgelöst.
    """
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Konfigurationsdatei '{CONFIG_FILE}' nicht gefunden. Bitte erstellen Sie sie mit dem gewünschten Dateinamen in der ersten Zeile.")
    with open(CONFIG_FILE, "r") as f:
        lines = f.read().splitlines()
        if len(lines) < 1 or not lines[0].strip():
            raise ValueError(f"Die erste Zeile in '{CONFIG_FILE}' muss den Dateinamen enthalten. Bitte tragen Sie dort den gewünschten Namen (z.B. 'cape.png') ein.")
        return lines[0].strip()

def get_target_dir():
    """
    Liest die zweite Zeile aus CONFIG_FILE und gibt sie zurück.
    Falls CONFIG_FILE fehlt oder die zweite Zeile fehlt/leer ist, wird ein Fehler ausgelöst.
    """
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Konfigurationsdatei '{CONFIG_FILE}' nicht gefunden. Bitte erstellen Sie sie mit dem Zielverzeichnis in der zweiten Zeile.")
    with open(CONFIG_FILE, "r") as f:
        lines = f.read().splitlines()
        if len(lines) < 2 or not lines[1].strip():
            raise ValueError(f"Die zweite Zeile in '{CONFIG_FILE}' muss das Zielverzeichnis enthalten. Bitte tragen Sie dort z.B. 'C:\\Users\\Benutzer\\AppData\\Roaming\\.minecraft\\assets\\skins\\87' ein.")
        return lines[1].strip()

def apply_selection(selected_file):
    target_dir = get_target_dir()
    os.makedirs(target_dir, exist_ok=True)

    for f in os.listdir(target_dir):
        try:
            os.remove(os.path.join(target_dir, f))
        except Exception:
            pass

    src = os.path.join(SOURCE_DIR, selected_file)
    dst_name = get_target_name()
    dst_path = os.path.join(target_dir, dst_name)
    shutil.copy(src, dst_path)


def open_image_zoomed(path, title="Vorschau"):
    img = Image.open(path)
    w, h = img.size
    zoom_factor = 8
    img = img.resize((w * zoom_factor, h * zoom_factor), Image.NEAREST)

    root = tk.Tk()
    root.title(title)
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=tk_img)
    label.pack()
    root.mainloop()

# === ASCII-Logo ===
def draw_ascii_logo(stdscr, start_y):
    logo = [
        " CCCC   A   PPP   EEEEE      CCCC H   H   A   N   N  GGGG EEEEE RRRR  ",
        "C      A A  P  P  E         C     H   H  A A  NN  N G     E     R   R ",
        "C     AAAAA PPP   EEE    -  C     HHHHH AAAAA N N N G  GG EEE   RRRR  ",
        "C     A   A P     E         C     H   H A   A N  NN G   G E     R  R  ",
        " CCCC A   A P     EEEEE      CCCC H   H A   A N   N  GGGG EEEEE R   R ",
    ]
    for i, line in enumerate(logo):
        stdscr.addstr(start_y + i, 2, line, curses.color_pair(5) | curses.A_BOLD)

# === Menu-list ===
def draw_menu(stdscr, files, current_index, selected_file, language):
    stdscr.clear()
    draw_ascii_logo(stdscr, 1)
    offset_y = 8

    for idx, file in enumerate(files):
        display_name = format_image_name(file, idx)

        if file == selected_file and idx == current_index:
            color = curses.color_pair(4)
        elif file == selected_file:
            color = curses.color_pair(3)
        elif idx == current_index:
            color = curses.color_pair(2)
        else:
            color = curses.color_pair(1)

        stdscr.attron(color)
        stdscr.addstr(offset_y + idx, 4, f"➤ {display_name}")
        stdscr.attroff(color)

    help_line_y = offset_y + len(files) + 1
    stdscr.addstr(help_line_y, 2, LANGUAGES[language]["help"])
    stdscr.refresh()

# === Main-Function ===
def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

    language = load_language()
    files = load_images()

    if not files:
        stdscr.addstr(2, 2, LANGUAGES[language]["no_files"])
        stdscr.refresh()
        stdscr.getch()
        return

    selected_file = load_state()
    current_index = 0
    if selected_file in files:
        current_index = files.index(selected_file)

    while True:
        draw_menu(stdscr, files, current_index, selected_file, language)

        key = stdscr.getch()
        if key == curses.KEY_UP:
            current_index = (current_index - 1) % len(files)
        elif key == curses.KEY_DOWN:
            current_index = (current_index + 1) % len(files)
        elif key in [curses.KEY_ENTER, 10, 13]:
            selected = files[current_index]
            apply_selection(selected)
            save_state(selected)
            selected_file = selected
        elif key in [ord('v'), ord('V')]:
            selected = files[current_index]
            open_image_zoomed(os.path.join(SOURCE_DIR, selected), LANGUAGES[language]["title"])
        elif key in [ord('l'), ord('L')]:
            language = "en" if language == "de" else "de"
            save_language(language)
        elif key in [ord('q'), ord('Q')]:
            break

# === Start ===
if __name__ == "__main__":
    os.makedirs(SOURCE_DIR, exist_ok=True)
    target_dir = get_target_dir()
    os.makedirs(target_dir, exist_ok=True)
    curses.wrapper(main)
