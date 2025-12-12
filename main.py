# Winfetch par JulioLeGrandSage - 2025 - Apache 2.0 License

import os
import sys
from PIL import Image
import platform
import psutil
import socket
import datetime

# Variables globales
ram_bytes = psutil.virtual_memory().total
ram_gb = round(ram_bytes / (1024 ** 3), 2)
cpu_name = platform.processor()
windows_version = platform.platform() 
ASCII_CHARS = "#$%&'()*+,-./:;<=>?@[]^_`{|}~"

disk_info = []  

def collect_disk_info():
    global disk_info
    disk_info = []
    partitions = psutil.disk_partitions()
    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            total_gb = round(usage.total / (1024**3), 2)
            used_gb = round(usage.used / (1024**3), 2)
            free_gb = round(usage.free / (1024**3), 2)
            percent = usage.percent

            disk_info.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "total": total_gb,
                "used": used_gb,
                "free": free_gb,
                "percent": percent
            })
        except PermissionError:
            disk_info.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "error": "Permission refusée"
            })

def get_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

def get_gpu_name():
    gpus = os.popen("wmic path win32_videocontroller get name").read().strip().split("\n")[1:]
    gpus = [gpu.strip() for gpu in gpus if gpu.strip()]
    return gpus

def draw_windows_logo_in_ascii():
    if getattr(sys, 'frozen', False):
        script_dir = sys._MEIPASS
    else:
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

def get_current_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

def main():
    draw_windows_logo_in_ascii()
    print("---------------------------------------------------------------")
    print(f"Current Date: {get_current_date()}")
    print(f"Current Time: {get_current_time()}")
    print("---------------------------------------------------------------")
    print(f"CPU: {cpu_name}")
    print(f"GPU: {', '.join(get_gpu_name())}")
    print(f"RAM: {ram_gb} GB")
    print(f"Windows Version: {windows_version}")
    print(" ")
    print(f"Disks Info:")
    collect_disk_info()
    for disk in disk_info:
        if "error" in disk:
            print(f"  {disk['device']} mounted on {disk['mountpoint']}: {disk['error']}")
        else:
            print(f"  {disk['device']} mounted on {disk['mountpoint']}: "
                  f"Total: {disk['total']} GB, Used: {disk['used']} GB ({disk['percent']}%), Free: {disk['free']} GB")
    print(" ")
    print("Network Info: ")
    get_network_info()
    print(f"  Hostname: {get_network_info()[0]}")
    print(f"  IP Address: {get_network_info()[1]}")

    input("\nAppuyez sur Entrée pour quitter...") 

if __name__ == "__main__":
    main()
