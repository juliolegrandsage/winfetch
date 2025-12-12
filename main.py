# Winfetch par JulioLeGrandSage - 2025 - Apache 2.0 License

import os
import sys
from PIL import Image
import platform
import psutil

# Variables globales
ram_bytes = psutil.virtual_memory().total
ram_gb = round(ram_bytes / (1024 ** 3), 2)
cpu_name = platform.processor()
windows_version = platform.platform()  # plus complet que platform.version()
ASCII_CHARS = "#$%&'()*+,-./:;<=>?@[]^_`{|}~"

def get_gpu_name():
    gpus = os.popen("wmic path win32_videocontroller get name").read().strip().split("\n")[1:]
    gpus = [gpu.strip() for gpu in gpus if gpu.strip()]
    return gpus

def draw_windows_logo_in_ascii():
    # Gestion du chemin compatible PyInstaller
    if getattr(sys, 'frozen', False):
        # Exécutable PyInstaller
        script_dir = sys._MEIPASS
    else:
        # Script Python normal
        script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "logo.png")

    img = Image.open(logo_path).convert("L")
    aspect_ratio = img.height / img.width
    new_width = 60
    new_height = int(aspect_ratio * new_width * 0.55)
    img = img.resize((new_width, new_height))

    pixels = img.getdata()
    ascii_str = "".join([ASCII_CHARS[pixel // 8] for pixel in pixels])

    for i in range(0, len(ascii_str), new_width):
        print(ascii_str[i:i + new_width])

def main():
    draw_windows_logo_in_ascii()
    print("---------------------------------------------------------------")
    print(f"CPU: {cpu_name}")
    print(f"GPU: {', '.join(get_gpu_name())}")
    print(f"RAM: {ram_gb} GB")
    print(f"Windows Version: {windows_version}")
    input("\nAppuyez sur Entrée pour quitter...")  # Permet de voir le terminal après double clic

if __name__ == "__main__":
    main()
