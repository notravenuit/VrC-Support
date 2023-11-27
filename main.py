import os
import ctypes
import sys
import webbrowser
import string
import random
import threading
import time
import subprocess
import tkinter as tk
import threading
import re
from datetime import datetime, timedelta
from github import Github
import requests
import zipfile
from io import BytesIO
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import pygetwindow as gw
import random   
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Listener
import shutil
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

if hasattr(sys, 'frozen'):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

mature_data_enabled = False
jp_lang_enabled = False
kr_lang_enabled = False
russian_lang_enabled = False
vng_logo_enabled = False
riot_client_name = "RiotClientUx.exe"
valorant_name = "VALORANT-Win64-Shipping.exe"
selected_language = ""
sfile = None
count = 0
source_folder1 = None
Ran = None
current_version = None
latest_version = None
def show_user_guide():
    # Hàm hiển thị hướng dẫn sử dụng
    user_guide = """
    Hướng dẫn sử dụng:
    - Bước 0: Đầu tiên bạn hãy ghi đường dẫn folder Valorant trên máy của bạn vào file ValorantPath.txt. Làm việc này sẽ giúp các lần sử dụng tới của bạn sẽ diễn ra nhanh hơn. Mặc định: C:\Valorant
    - Bước 1: Nhấn nút "Đọc từ file ValorantPath.txt" để chọn Thư mục Valorant 1 cách nhanh chóng. Bạn cũng có thể nhấn nút "Chọn Thư mục" nếu như bạn chưa thiết lập trước đó
    - Bước 2: Chọn tính năng bạn muốn sử dụng
        + Nếu bạn muốn bật tính năng Máu/Xác trong VALORANT, hãy nhấn nút "Hiển thị Máu/Xác"
        + Thay đổi ngôn ngữ âm thanh trong VALORANT sang tiếng Nhật, tiếng Hàn..., hãy nhấn nút "Thay đổi Voice"
    """ 
    messagebox.showinfo("Hướng dẫn sử dụng", user_guide)

def copy_files_to_valorant_folder(source_folder):
    # Hàm sao chép các tệp .pak và .sig vào thư mục VALORANT
    try:
        source_bin_folder = os.path.join(os.path.dirname("."), "bin")
        destination_bin_folder = os.path.join(source_folder, "live", "ShooterGame", "Content", "Paks")
        shutil.copy(os.path.join(source_bin_folder, "MatureData-WindowsClient.pak"), os.path.join(destination_bin_folder, "MatureData-WindowsClient.pak"))
        shutil.copy(os.path.join(source_bin_folder, "MatureData-WindowsClient.sig"), os.path.join(destination_bin_folder, "MatureData-WindowsClient.sig"))
        print("Sao chep Mature")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")

def copy_logo_files(source_folder):
    # Hàm sao chép các tệp .pak và .sig vào thư mục VALORANT
    try:
        source_bin_folder = os.path.join(os.path.dirname("."), "bin")
        destination_bin_folder = os.path.join(source_folder, "live", "ShooterGame", "Content", "Paks")
        shutil.copy(os.path.join(source_bin_folder, "VNGLogo-WindowsClient.pak"), os.path.join(destination_bin_folder, "VNGLogo-WindowsClient.pak"))
        shutil.copy(os.path.join(source_bin_folder, "VNGLogo-WindowsClient.sig"), os.path.join(destination_bin_folder, "VNGLogo-WindowsClient.sig"))
        print("Sao chep logo file")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi: {str(e)}.\nTính năng Hiển thị Máu/Xác sẽ tiếp tục được bật")

def remove_files(source_folder):
    destination_bin_folder = os.path.join(source_folder, "live", "ShooterGame", "Content", "Paks")
    
    files_to_remove = [
        "VNGLogo-WindowsClient.pak",
        "VNGLogo-WindowsClient.sig"
    ]
    
    for file_name in files_to_remove:
        file_path = os.path.join(destination_bin_folder, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)

def remove_file_VNG():
    global vng_logo_enabled
    source_folder = entry_source_folder.get()
    if not source_folder:
        messagebox.showerror("Lỗi", "Vui lòng nhập thư mục Valorant.")
        return

    if os.path.exists(source_folder):
        if vng_logo_enabled:
            if mature_data_enabled:
                messagebox.showinfo("Thông báo", "Bạn không thể tắt khi tính năng 'Hiển thị Máu/Xác': ON.")
            else:
                vng_logo_enabled = False
                button_logo.config(text="Ẩn Logo VNG: OFF")
                copy_logo_files(source_folder)
        else:
            if mature_data_enabled:
                messagebox.showinfo("Thông báo", "Tính năng đã được bật sẵn khi tính năng 'Hiển thị Máu/Xác': ON.")                
            else:
                vng_logo_enabled = True
                button_logo.config(text="Ẩn Logo VNG: ON")
                remove_files(source_folder)
    else:
        messagebox.showerror("Lỗi", "Vui lòng kiểm tra thư mục Valorant.")

source_folder = ""

def select_source_folder():
    global source_folder
    # source_folder1 = os.path.dirname(filedialog.askdirectory())
    source_folder1 = filedialog.askdirectory()
    source_folder = source_folder1
    if source_folder:
        entry_source_folder.delete(0, tk.END)
        entry_source_folder.insert(0, source_folder)
        sfile = source_folder  # Đảm bảo rằng biến sfile được gán giá trị mới nếu cần.
    return source_folder

def read_source_folder_from_file():
    global source_folder
    try:
        with open("ValorantPath.txt", "r") as file:
            # source_folder1 = os.path.dirname(file.read().strip())
            source_folder1 = file.read().strip()
            source_folder = source_folder1
            entry_source_folder.delete(0, tk.END)
            entry_source_folder.insert(0, source_folder)
            sfile = source_folder  # Đảm bảo rằng biến sfile được gán giá trị mới nếu cần.
        return source_folder
    except FileNotFoundError:
        messagebox.showerror("Lỗi", "Tệp ValorantPath.txt không tồn tại.")

def execute_copy_and_remove():
    global mature_data_enabled
    source_folder = entry_source_folder.get()
    if not source_folder:
        messagebox.showerror("Lỗi", "Vui lòng nhập thư mục Valorant.")
        return

    if os.path.exists(source_folder):
        if mature_data_enabled:
            mature_data_enabled = False
            button_execute.config(text="Hiển thị Máu/Xác: OFF")
            copy_logo_files(source_folder)
        else:
            mature_data_enabled = True
            button_execute.config(text="Hiển thị Máu/Xác: ON")
            copy_files_to_valorant_folder(source_folder)
            remove_files(source_folder)
    else:
        messagebox.showerror("Lỗi", "Vui lòng kiểm tra thư mục Valorant.")

user_guide_text_mac_dinh = """
LƯU Ý: Bạn phải chuyển ngôn ngữ của Valorant sang tiếng bạn muốn bằng Riot Client hoặc VALORANT trước. Nếu không tính năng sẽ không thể hoạt động thành công!!
"""

def open_audio_window():
    global audio_window
    button_audio.config(state="disabled")
    source_folder = entry_source_folder.get()
    if not source_folder:
        messagebox.showerror("Lỗi", "Vui lòng nhập thư mục Valorant.")
        return

    def confirm_action():
        nonlocal source_folder
        global selected_o
        selected_o = o_var.get()
        if source_folder:
            process_selection(selected_o, source_folder)
            audio_window.withdraw()
            button_audio.config(state="normal")
    def on_closing():
        button_audio.config(state="normal")
        audio_window.destroy()
    audio_window = tk.Toplevel(root)
    audio_window.title("Danh sách ngôn ngữ")
    audio_window.protocol("WM_DELETE_WINDOW", on_closing)
    frame = ttk.LabelFrame(audio_window, text="Chọn Ngôn ngữ")
    frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

    label_o = ttk.Label(frame, text="Ngôn ngữ âm thanh:")
    label_o.grid(row=1, column=0, padx=10, pady=5)

    o_var = tk.StringVar()
    o_menu = ttk.Combobox(frame, textvariable=o_var, values=["Tiếng Nhật", "Tiếng Hàn", "Tiếng Nga"])
    o_menu.grid(row=1, column=1, padx=10, pady=5)
    o_menu.set("Tiếng Nhật")

    confirm_button = ttk.Button(audio_window, text="Xác nhận", command=confirm_action)
    confirm_button.grid(row=1, column=0, columnspan=2, pady=10)
    
    # Label cho hướng dẫn
    user_guide_label = tk.Label(audio_window, text=user_guide_text_mac_dinh, justify="left")
    user_guide_label.grid(row=2, column=0, padx=20, pady=10, columnspan=2)

    def update_user_guide():
        selected_language = o_var.get()
        user_guide_label.config(text=user_guide_text_mac_dinh)

    o_var.trace("w", lambda *args: update_user_guide())

def process_selection(selected_o, source_folder):
    global selected_language, jp_lang_enabled, kr_lang_enabled, russian_lang_enabled
    if selected_o == "Tiếng Nhật":
        copy_vietnamese_japanese_files(source_folder)
        jp_lang_enabled = True
        selected_language = selected_o
        jp_language_thread = threading.Thread(target=check_and_set_japanese_language)
        jp_language_thread.daemon = True
        jp_language_thread.start()

    elif selected_o == "Tiếng Hàn":
        copy_vietnamese_korean_files(source_folder)
        kr_lang_enabled = True
        selected_language = selected_o
        kr_language_thread = threading.Thread(target=check_and_set_korean_language)
        kr_language_thread.daemon = True
        kr_language_thread.start()
    elif selected_o == "Tiếng Nga":
        copy_vietnamese_russian_files(source_folder)
        russian_lang_enabled = True
        selected_language = selected_o
        russian_language_thread = threading.Thread(target=check_and_set_russian_language)
        russian_language_thread.daemon = True
        russian_language_thread.start()
    else:
        messagebox.showinfo("Thông báo", "Không có thay đổi nào.")


def copy_vietnamese_japanese_files(source_folder):
    source_jpy = os.path.join(".", "bin", "vie-jpy")
    destination_folder = os.path.join(source_folder, "live", "ShooterGame", "Content", "Paks")

    try:
        shutil.copy(os.path.join(source_jpy, "ja_JP_Text-WindowsClient.pak"), os.path.join(destination_folder, "ja_JP_Text-WindowsClient.pak"))
        shutil.copy(os.path.join(source_jpy, "ja_JP_Text-WindowsClient.sig"), os.path.join(destination_folder, "ja_JP_Text-WindowsClient.sig"))
        if not check_icon:
            button_audio.config(text="Thay đổi Voice: ON\nNgôn ngữ: Tiếng Nhật")
        print("reload jp")
    except Exception as e:
        if not check_icon:
            button_audio.config(f"Thay đổi Voice: OFF\nLỗi khi sử dụng Voice tiếng Nhật: {str(e)}")
def vie_jp(source_folder):
    source_jpy = os.path.join(".", "bin", "vie-jpy")
    destination_folder = os.path.join(source_folder, "live", "ShooterGame", "Content", "Paks")
    shutil.copy(os.path.join(source_jpy, "ja_JP_Text-WindowsClient.pak"), os.path.join(destination_folder, "ja_JP_Text-WindowsClient.pak"))
    shutil.copy(os.path.join(source_jpy, "ja_JP_Text-WindowsClient.sig"), os.path.join(destination_folder, "ja_JP_Text-WindowsClient.sig"))
    print("reload jp")
def copy_vietnamese_korean_files(source_folder):
    source_kor = os.path.join(".", "bin", "vie-jpy")
    destination_folder = os.path.join(source_folder, "live", "ShooterGame", "Content", "Paks")

    try:
        shutil.copy(os.path.join(source_kor, "ja_JP_Text-WindowsClient.pak"), os.path.join(destination_folder, "ko_KR_Text-WindowsClient.pak"))
        shutil.copy(os.path.join(source_kor, "ja_JP_Text-WindowsClient.sig"), os.path.join(destination_folder, "ko_KR_Text-WindowsClient.sig"))
        if not check_icon:
            button_audio.config(text="Thay đổi Voice: ON\nNgôn ngữ: Tiếng Hàn")
        print("reload kr")
    except Exception as e:
        if not check_icon:
            button_audio.config(f"Thay đổi Voice: OFF\nLỗi khi sử dụng Voice tiếng Hàn: {str(e)}")
def vie_kor(source_folder):
    source_kor = os.path.join(".", "bin", "vie-jpy")
    destination_folder = os.path.join(source_folder, "live", "ShooterGame", "Content", "Paks")
    shutil.copy(os.path.join(source_kor, "ja_JP_Text-WindowsClient.pak"), os.path.join(destination_folder, "ko_KR_Text-WindowsClient.pak"))
    shutil.copy(os.path.join(source_kor, "ja_JP_Text-WindowsClient.sig"), os.path.join(destination_folder, "ko_KR_Text-WindowsClient.sig"))
    print("reload kr")

    print("reload jp")
def copy_vietnamese_russian_files(source_folder):
    source_rus = os.path.join(".", "bin", "vie-jpy")
    destination_folder = os.path.join(source_folder, "live", "ShooterGame", "Content", "Paks")

    try:
        shutil.copy(os.path.join(source_rus, "ja_JP_Text-WindowsClient.pak"), os.path.join(destination_folder, "ru_RU_Text-WindowsClient.pak"))
        shutil.copy(os.path.join(source_rus, "ja_JP_Text-WindowsClient.sig"), os.path.join(destination_folder, "ru_RU_Text-WindowsClient.sig"))
        if not check_icon:
            button_audio.config(text="Thay đổi Voice: ON\nNgôn ngữ: Tiếng Nga")
        print("reload rs")
    except Exception as e:
        if not check_icon:
            button_audio.config(f"Thay đổi Voice: OFF\nLỗi khi sử dụng Voice tiếng Nga: {str(e)}")

def vie_rus(source_folder):
    source_rus = os.path.join(".", "bin", "vie-jpy")
    destination_folder = os.path.join(source_folder, "live", "ShooterGame", "Content", "Paks")
    shutil.copy(os.path.join(source_rus, "ja_JP_Text-WindowsClient.pak"), os.path.join(destination_folder, "ru_RU_Text-WindowsClient.pak"))
    shutil.copy(os.path.join(source_rus, "ja_JP_Text-WindowsClient.sig"), os.path.join(destination_folder, "ru_RU_Text-WindowsClient.sig"))
    print("reload rs")

def check_and_execute_mature_data():
    global mature_data_enabled
    while True:
        time.sleep(3)  # Kiểm tra mỗi 5 giây
        riot_client_running = any(process.info['name'] == riot_client_name for process in psutil.process_iter(attrs=['name']))
        valorant_running = any(process.info['name'] == valorant_name for process in psutil.process_iter(attrs=['name']))
    
        if mature_data_enabled and riot_client_running and not valorant_running:
            copy_files_to_valorant_folder(source_folder)
            remove_files(source_folder)

mature_data_thread = threading.Thread(target=check_and_execute_mature_data)
mature_data_thread.daemon = True
mature_data_thread.start()


def check_and_remove_logo_files():
    global vng_logo_enabled
    while True:
        time.sleep(3)  # Kiểm tra mỗi 5 giây
        riot_client_running1 = any(process.info['name'] == riot_client_name for process in psutil.process_iter(attrs=['name']))
        valorant_running1 = any(process.info['name'] == valorant_name for process in psutil.process_iter(attrs=['name']))
        # Kiểm tra xem process "RiotClientUx.exe" có đang chạy hay không
        if vng_logo_enabled and riot_client_running1 and not valorant_running1:
            remove_files(source_folder)


def check_and_set_japanese_language():
    global jp_lang_enabled, source_folder
    while True:
        time.sleep(3)  # Kiểm tra mỗi 5 giây
        riot_client_running2 = any(process.info['name'] == riot_client_name for process in psutil.process_iter(attrs=['name']))
        valorant_running2 = any(process.info['name'] == valorant_name for process in psutil.process_iter(attrs=['name']))
        if jp_lang_enabled and riot_client_running2 and not valorant_running2:
            vie_jp(source_folder)
            
            # Sau khi thay đổi, có thể sử dụng các hàm hoặc thông báo tương tự như đã làm ở các ví dụ trước

# Chức năng kiểm tra và thay đổi ngôn ngữ sang tiếng Hàn
def check_and_set_korean_language():
    global kr_lang_enabled
    while True:
        time.sleep(3)  # Kiểm tra mỗi 5 giây
        riot_client_running3 = any(process.info['name'] == riot_client_name for process in psutil.process_iter(attrs=['name']))
        valorant_running3 = any(process.info['name'] == valorant_name for process in psutil.process_iter(attrs=['name']))
        if kr_lang_enabled and riot_client_running3 and not valorant_running3:
            vie_kor(source_folder) 
            
            # Sau khi thay đổi, có thể sử dụng các hàm hoặc thông báo tương tự như đã làm ở các ví dụ trước

def check_and_set_russian_language():
    global russian_lang_enabled
    while True:
        time.sleep(3)  # Kiểm tra mỗi 5 giây
        riot_client_running = any(process.info['name'] == riot_client_name for process in psutil.process_iter(attrs=['name']))
        valorant_running = any(process.info['name'] == valorant_name for process in psutil.process_iter(attrs=['name']))
        if russian_lang_enabled and riot_client_running and not valorant_running:
            vie_rus(source_folder) 

def terminate_process(process):
        process.terminate()

def kill_processes(process_names):
    for name in process_names:
        for process in psutil.process_iter(attrs=['name']):
            if name.lower() in process.info['name'].lower():
                # Sử dụng thread riêng cho từng tiến trình
                thread = threading.Thread(target=terminate_process, args=(process,))
                thread.start()

def kill_process_valorant():
    # Danh sách tên các tiến trình bạn muốn tắt
    processes_to_kill = ['RiotClientUx.exe', 'RiotClientServices.exe', 'VALORANT-Win64-Shipping.exe', 'RiotClientCrashHandler.exe']
    
    # Gọi hàm để tắt các tiến trình
    try:
        kill_processes(processes_to_kill)
        tk.messagebox.showinfo("Thông báo", "Đã hoàn thành tắt các process liên quan tới VALORANT.")
    except:
        tk.messagebox.showinfo("Thông báo", "Thất bại. Có thể hệ thống máy tính bạn đang không hề bật VALORANT")

# Rest of the code remains the same.

def open_link_in_browser(url):
    try:
        # Thử mở Chrome với URL cụ thể
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        subprocess.Popen([chrome_path, url], shell=True)
    except FileNotFoundError:
        # Nếu Chrome chưa được cài đặt, sử dụng webbrowser để mở liên kết
        webbrowser.open(url)

searching = False  # Biến cờ để theo dõi trạng thái tìm kiếm

def search_for_valorant(drive, result_file_path):
    cmd = f'dir {drive} /s /b | findstr /i "VALORANT.exe"'
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    if result.returncode == 0:
        paths = result.stdout.splitlines()
        for path in paths:
            if os.path.exists(path):
                live_folder = os.path.join(os.path.dirname(path), "ShooterGame", "Content", "Paks")
                print(live_folder)

                if os.path.exists(live_folder) and os.path.isdir(live_folder):
                    with open(result_file_path, 'w') as result_file:
                        result_file.write(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(live_folder)))))
                        print(f"result file: {os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(live_folder))))}")
    else:
        print(f"Error: {result.stderr}")


search_lock = threading.Lock()
def auto_find_vlr_path():
    global searching  # Sử dụng biến cờ global

    if searching:
        return  # Không làm gì nếu đang tìm kiếm

    searching = True  # Đang tìm kiếm

    # Vô hiệu hóa nút "Tìm kiếm"
    button_auto_find_vlr_path.config(state="disabled")
    button_auto_find_vlr_path.config(text="Đang tìm kiếm folder VALORANT... Vui lòng chờ!")

    drives = ['A:\\', 'B:\\', 'C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\', 'I:\\', 'J:\\', 'K:\\', 'L:\\', 'M:\\', 'N:\\', 'O:\\', 'P:\\', 'Q:\\', 'R:\\', 'S:\\', 'T:\\', 'U:\\', 'V:\\', 'W:\\', 'X:\\', 'Y:\\', 'Z:\\']

    result_file_path = './bin/valorant_paths.txt'


    search_thread = threading.Thread(target=perform_search, args=(drives, result_file_path))
    search_thread.start()
    messagebox.showinfo("Thông báo", "Sẽ mất một lúc để hệ thống tìm kiếm.\nTrong lúc đó các bạn hãy xem các bộ Keycap Valorant mà Virodict đang bán và mua ủng hộ bọn mình nếu có thể nha ♥")
    open_link_in_browser("https://bit.ly/keycapvalorant")
def perform_search(drives, result_file_path):
    processes = []
    for drive in drives:
        process = threading.Thread(target=search_for_valorant, args=(drive, result_file_path))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    try:
        shutil.copy(result_file_path, "ValorantPath.txt")
        messagebox.showinfo("Thông báo", "Thành công! Ứng dụng sẽ tự động khởi động lại")
        python = sys.executable
        os.execl(python, python, *sys.argv)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tìm thấy! {str(e)}")

    global searching
    searching = False  # Đã hoàn thành tìm kiếm

    # Kích hoạt lại nút "Tìm kiếm"
    button_auto_find_vlr_path.config(state="normal")



tray_icon = None
check_icon = None
def on_show_window_clicked():
    global tray_icon
    global check_icon
    root.deiconify()  # Hiển thị ứng dụng khi người dùng nhấn vào biểu tượng
    tray_icon.stop()  # Dừng biểu tượng trong System Tray
    show_taskbar_logo()
    check_icon = False
def hide_console_window():
    # Ẩn cửa sổ console nếu có
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def on_hide_window_clicked():
    global tray_icon
    global check_icon
    tray_icon = icon("name", image1, menu=menu(item('Hiển thị', on_show_window_clicked)))
    root.withdraw()  # Ẩn ứng dụng khi người dùng nhấn vào nút "Chạy ngầm tool"
    tray_icon.run()
    check_icon = True

def on_tray_icon_double_click():
    on_show_window_clicked()

def hide_taskbar_logo():
    root.overrideredirect(True)  # Ẩn logo trên thanh taskbar
    root.withdraw()

def show_taskbar_logo():
    root.overrideredirect(False)  # Hiển thị lại logo trên thanh taskbar
    root.deiconify()

def create_tray_icon():
    global tray_icon
    tray_icon = icon("VrC Support", image1, menu=menu(item('Hiển thị ứng dụng', on_show_window_clicked)))
    root.after(100, app_thread)
    tray_icon.double_click = on_tray_icon_double_click  # Gán hàm xử lý cho sự kiện double click
    return tray_icon



def download_and_extract_zip(url, destination):
    response = requests.get(url)

    # Sử dụng threading để giải nén mà không làm treo ứng dụng
    thread = threading.Thread(target=extract_zip, args=(BytesIO(response.content), destination))
    thread.start()

def extract_zip(zip_data, destination):
    with zipfile.ZipFile(zip_data, "r") as zip_ref:
        zip_ref.extractall(destination)

def keep_specific_folders():
    current_version = "2.5"
    # Lấy danh sách tất cả các thư mục trong thư mục cơ sở
    base_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    all_folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    # Đường dẫn đến thư mục cơ sở (Vd: 'VrC')

    # Danh sách các thư mục cụ bạn muốn giữ lại (Vd: ['VrC-Support_2.2'])
    folders_to_keep = [f'VrC-Support_{current_version}']
    # Biểu thức chính quy để kiểm tra xem một thư mục có bắt đầu bằng 'VrC-Support' hay không
    pattern = re.compile(r'^VrC-Support')

    # Xóa các thư mục không chứa từ khóa và không nằm trong danh sách giữ lại
    for folder in all_folders:
        if pattern.match(folder) and folder not in folders_to_keep:
            folder_path = os.path.join(base_folder, folder)
            shutil.rmtree(folder_path)
            print(f"Da xoa thu muc: {folder_path}")



def disable_all_buttons(button_list):
    for button in button_list:
        button["state"] = "disabled"

def update_application():
    global latest_version
    current_version = "2.5"  # Phiên bản hiện tại (đọc từ tệp tin hoặc thông tin ứng dụng)
    script_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    # Thông tin tài khoản GitHub và repository
    github_token = "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"  # Cung cấp token để có quyền truy cập vào GitHub API
    repo_owner = "notravenuit"
    repo_name = "VrC-Support"
    g = Github(github_token)
    # Lấy repository
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    # Lấy thông tin release
    latest_release = repo.get_latest_release()
    latest_version = latest_release.tag_name
    folder_path = os.path.join(script_directory,"VrC-Support_" + latest_version, )
    with open("./bin/check.txt", "r") as file:
            checkver = file.read()
    if checkver == "True":
        with open("./bin/check.txt", "w") as file:
            file.write("False")
        keep_specific_folders()
    if latest_version > current_version:
        # Hiển thị thông báo "Đang tự động update"
        disable_all_buttons(all_buttons)
        messagebox.showinfo("Thông báo", f"Đang tự động update Version {latest_version}. \nVUI LÒNG KHÔNG MỞ LẠI TOOL TRONG QUÃNG THỜI GIAN NÀY")
        # Lấy danh sách assets
        assets = latest_release.get_assets()

        # Kiểm tra xem danh sách assets có tệp tin không
        if assets.totalCount > 0:
            # Lấy URL tải xuống của phiên bản mới từ asset đầu tiên
            download_url = assets[0].browser_download_url

            # Tiếp tục xử lý...
            print(f"Download URL: {download_url}")

            # Thực hiện cập nhật
            download_and_extract_zip(download_url, os.path.join(script_directory, "VrC-Support_" + latest_version))  # Thay đổi thành thư mục ứng dụng của bạn
            # Hiển thị thông báo "Đã update xong"
            messagebox.showinfo("Thông báo", f"Đã update xong phiên bản {latest_version}.\nHệ thống sẽ tự động mở thư mục phiên bản mới cho bạn")
            if os.name == 'nt':  # 'nt' là mã định danh cho Windows
                    cmd = f'start {folder_path}'
                    subprocess.run(cmd, shell=True, text=True, capture_output=True)
            cmd = f'taskkill /f /im "VrC Support.exe"'
            subprocess.run(cmd, shell=True, text=True, capture_output=True)
            root.protocol("WM_DELETE_WINDOW", sys.exit())

def clean_up_temp_folder():
    # Lấy danh sách tất cả các thư mục trong thư mục cơ sở
    base_folder = os.path.dirname(os.path.dirname(__file__))
    folders_to_keep = [os.path.basename(os.path.dirname(__file__))]
    all_folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
    # Biểu thức chính quy để kiểm tra xem một thư mục có bắt đầu bằng 'VrC-Support' hay không
    pattern = re.compile(r'^_MEI')

    # Xóa các thư mục không chứa từ khóa và không nằm trong danh sách giữ lại
    for folder in all_folders:
        if pattern.match(folder) and folder not in folders_to_keep:
            folder_path = os.path.join(base_folder, folder)
            time.sleep(1)
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                try:
                    shutil.rmtree(folder_path)
                    print(f"Đã xóa thư mục: {folder_path}")
                except Exception as e:
                    print(f"Lỗi khi xóa thư mục {folder_path}: {e}")

def app_thread():
    root.mainloop()
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Virodict Support - 2.5")

    for i in range(3):
        root.grid_rowconfigure(i, weight=1)
    for i in range(3):
        root.grid_columnconfigure(i, weight=1)



    check = False
        
    bank_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin", "bank.png")
    icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin", "icon.ico")
    root.iconbitmap(default=icon_path)
    image1 = Image.open(icon_path)
    # tray_icon = create_tray_icon()
    # root.after(100, app_thread)
    root.deiconify()
    # clean_up_temp_folder()
    # Khung chứa nút và tiêu đề
    frame_title = ttk.LabelFrame(root, text="Hướng dẫn và Lưu ý")
    frame_title.grid(row=0, column=0, columnspan=3, padx=20, pady=10, sticky="we")


    # Nút Hướng dẫn sử dụng
    button_user_guide = ttk.Button(frame_title, text="Hướng dẫn sử dụng", command=show_user_guide)
    button_user_guide.grid(row=0, column=0, padx=10, pady=10)

    button_detailed_guide = ttk.Button(frame_title, text="Hướng dẫn chi tiết", command=lambda: open_link_in_browser("https://github.com/notravenuit/VrC-Support"))
    button_detailed_guide.grid(row=0, column=1, padx=10, pady=10)

    button_hide_app = ttk.Button(root, text="Chạy ngầm Tool", command=on_hide_window_clicked)
    button_hide_app.grid(row=0, column=6, padx=10, pady=10)  # Sử dụng grid thay vì pack

    # button_quest = ttk.Button(frame_title, text=f"Lượt sử dụng còn lại: {count_value}")
    # button_quest.grid(row=0, column=2, padx=10, pady=10)

    label_below_buttons = ttk.Label(frame_title, text="""LƯU Ý: Sử dụng và bật tính năng Tool trước khi vào VALORANT""")
    label_below_buttons.grid(row=1, columnspan=2, pady=5)

    # Khung Thư mục Valorant
    frame_source_folder = ttk.LabelFrame(root, text="Thư mục nguồn")
    frame_source_folder.grid(row=1, column=0, padx=20, pady=10, sticky="we")


    label_source_folder = ttk.Label(frame_source_folder, text="Thư mục Valorant:")
    label_source_folder.grid(row=0, column=0, sticky="w")

    entry_source_folder = ttk.Entry(frame_source_folder, width=40)
    entry_source_folder.grid(row=0, column=1, sticky="w")

    button_select_source_folder = ttk.Button(frame_source_folder, text="Chọn Thư mục", command=select_source_folder)
    button_select_source_folder.grid(row=0, column=2, padx=10)

    button_auto_find_vlr_path = ttk.Button(frame_source_folder, text="Tự động tìm kiếm folder VALORANT", command=auto_find_vlr_path)
    button_auto_find_vlr_path.grid(row=0, column=3, padx=10)


    button_read_from_file = ttk.Button(frame_source_folder, text="Đọc từ file ValorantPath.txt", command=read_source_folder_from_file)
    button_read_from_file.grid(row=0, column=4, padx=10)

    # Khung tính năng
    frame_features = ttk.LabelFrame(root, text="Tính năng")
    frame_features.grid(row=2, column=0, padx=20, pady=10, sticky="w")

    button_execute = ttk.Button(frame_features, text="Hiển thị Máu/Xác: OFF", command=execute_copy_and_remove)
    button_execute.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    button_audio = ttk.Button(frame_features, text="Thay đổi Voice: OFF", command=open_audio_window)
    button_audio.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    button_logo = ttk.Button(frame_features, text="Ẩn Logo VNG: OFF", command=remove_file_VNG)
    button_logo.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    button_process = ttk.Button(frame_features, text="Tắt VALORANT & Riot Client", command=kill_process_valorant)
    button_process.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    image = Image.open(bank_path)
    desired_size = (330, 400)
    resized_image = image.resize(desired_size, Image.BICUBIC)
    photo = ImageTk.PhotoImage(resized_image)

    # Tạo ttk.LabelFrame
    frame_links = ttk.LabelFrame(root, text="Liên kết")
    frame_links.grid(row=3, column=0, padx=20, pady=10, sticky="we")

    # Tạo ttk.Label để hiển thị ảnh
    label_image = ttk.Label(frame_links, image=photo)
    label_image.grid(row=0, column=0, padx=5, pady=5, rowspan=4)  # Sử dụng rowspan để kéo dài ảnh qua nhiều dòng

    # Tạo các nút và đặt chúng trong frame_links
    button_donate = ttk.Button(frame_links, text="Donate", command=lambda: open_link_in_browser("https://beacons.ai/notravenuit"))
    button_donate.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    button_support = ttk.Button(frame_links, text="Hỗ trợ qua Discord", command=lambda: open_link_in_browser("https://discord.gg/sPqfg5FZcn"))
    button_support.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    button_buy_keycap = ttk.Button(frame_links, text="Mua Keycap Valorant", command=lambda: open_link_in_browser("https://shopee.ee/5AJIjrtTIw"))
    button_buy_keycap.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    button_youtube = ttk.Button(frame_links, text="YouTube", command=lambda: open_link_in_browser("https://www.youtube.com/notravenuit"))
    button_youtube.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    all_buttons = [
        button_user_guide,
        button_detailed_guide,
        button_hide_app,
        button_select_source_folder,
        button_auto_find_vlr_path,
        button_read_from_file,
        button_execute,
        button_audio,
        button_logo,
        button_process,
        button_donate,
        button_support,
        button_buy_keycap,
        button_youtube
    ]
    # Đặt frame_links trong root
    frame_links.grid(row=3, column=0, padx=20, pady=10, sticky="we")
    update_application__thread = threading.Thread(target=update_application)
    update_application__thread.daemon = True
    update_application__thread.start()
    source_folder = read_source_folder_from_file()
    if not source_folder: 
        select_source_folder()
    random_number = random.randint(1, 5)
    if random_number == 1:
            messagebox.showinfo("LƯU Ý", "Tham gia Server Discord để nhận nhiều đặc quyền, tính năng và thường xuyên tham gia Give Away\nLink tại phần Liên kết")
    root.mainloop()