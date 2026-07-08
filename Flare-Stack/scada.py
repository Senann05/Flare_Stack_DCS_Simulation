import serial
import customtkinter as ctk
import csv
import threading
import time
import os  
from datetime import datetime, timedelta

PORT = "COM5" 
BAUD = 9600
CSV_FILE = "flare_stack_hourly_report.csv"

simulated_time = datetime(2026, 5, 7, 14, 0, 0)
current_mode = "DAY"

last_status = "NORMAL"
last_flame = 0
last_limit = 0

with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Report Timestamp", "Shift Mode", "Safety Status", "Flame Level (Raw)", "Active Limit"])

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("550x620") 
app.title("🔥 Enterprise Flare Stack DCS Panel")

header_frame = ctk.CTkFrame(app, corner_radius=10)
header_frame.pack(pady=10, padx=20, fill="x")

title_label = ctk.CTkLabel(header_frame, text="Hourly Commercial Accounting System", font=("Arial", 16, "bold"))
title_label.pack(pady=(10, 0))

time_label = ctk.CTkLabel(header_frame, text="System Time: 07.05.2026 - 14:00", font=("Consolas", 16), text_color="#00FFFF")
time_label.pack(pady=5)

mode_label = ctk.CTkLabel(header_frame, text="Mode: DAY", font=("Consolas", 14, "bold"))
mode_label.pack(pady=(0, 10))

level_label = ctk.CTkLabel(app, text="Flame Level: 0", font=("Arial", 15))
level_label.pack(pady=5)

level_progressbar = ctk.CTkProgressBar(app, width=350, height=15)
level_progressbar.pack(pady=5)
level_progressbar.set(0)

limit_label = ctk.CTkLabel(app, text="Active Limit: 0", font=("Arial", 13), text_color="#FFA500")
limit_label.pack(pady=5)

status_frame = ctk.CTkFrame(app, width=350, height=65, corner_radius=10)
status_frame.pack(pady=15)
status_frame.pack_propagate(False)

status_label = ctk.CTkLabel(status_frame, text="CONNECTING TO DCS...", font=("Arial", 16, "bold"))
status_label.place(relx=0.5, rely=0.5, anchor="center")

control_frame = ctk.CTkFrame(app, corner_radius=10)
control_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(control_frame, text="Remote Manual Override", font=("Arial", 13, "bold")).pack(pady=5)

def send_mute_cmd():
    if ser and ser.is_open: ser.write(b"MUTE\n")

def send_led_cmd():
    if ser and ser.is_open: ser.write(b"LED\n")

btn_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
btn_frame.pack(pady=10)

mute_btn = ctk.CTkButton(btn_frame, text="🔊 BUZZER ON", fg_color="#2B2B2B", command=send_mute_cmd)
mute_btn.pack(side="left", padx=10)

led_btn = ctk.CTkButton(btn_frame, text="💡 LEDS ENABLED", fg_color="#2B2B2B", command=send_led_cmd)
led_btn.pack(side="left", padx=10)


report_frame = ctk.CTkFrame(app, fg_color="transparent")
report_frame.pack(pady=10)

def open_report():
    try:
        os.startfile(CSV_FILE)
    except Exception as e:
        print(f"Report file not found or could not be opened: {e}")

report_btn = ctk.CTkButton(report_frame, text="📊 OPEN COMMERCIAL REPORT", font=("Arial", 14, "bold"), fg_color="#1E90FF", hover_color="#4169E1", height=40, width=250, command=open_report)
report_btn.pack()

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except Exception:
    status_label.configure(text="HARDWARE DISCONNECTED", text_color="red")
    ser = None

def advance_simulated_time_and_log():
    global simulated_time, current_mode
    while True:
        time.sleep(5)
        simulated_time += timedelta(hours=1)
        
        hour = simulated_time.hour
        new_mode = "DAY" if 6 <= hour < 18 else "NIGHT"
            
        if new_mode != current_mode:
            current_mode = new_mode
            if ser and ser.is_open:
                ser.write(f"MODE:{current_mode}\n".encode('utf-8'))
        
        log_hourly_commercial_data()
        
        app.after(0, update_time_ui)

def log_hourly_commercial_data():
    time_str = simulated_time.strftime("%d.%m.%Y - %H:%M")
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([time_str, current_mode, last_status, last_flame, last_limit])

def update_time_ui():
    time_label.configure(text=f"System Time: {simulated_time.strftime('%d.%m.%Y - %H:%M')}")
    mode_color = "#FFD700" if current_mode == "DAY" else "#4169E1"
    mode_label.configure(text=f"Active Shift: {current_mode}", text_color=mode_color)

def read_from_arduino():
    global last_status, last_flame, last_limit
    while ser and ser.is_open:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(":")
                if len(parts) == 5:
                    status, flame_raw, limit_raw, mute_state, led_state = parts
                    
                    last_status = status
                    last_flame = int(flame_raw)
                    last_limit = int(limit_raw)
                    
                    app.after(0, update_ui, status, last_flame, last_limit, mute_state, led_state)
        except Exception:
            pass

def update_ui(status, flame_val, limit_val, mute_state, led_state):
    level_progressbar.set(flame_val / 1023.0)
    level_label.configure(text=f"Flame Level: {flame_val} / 1023")
    limit_label.configure(text=f"Active Limit: {limit_val}")

    if status == "ALARM":
        status_label.configure(text="⚠️ FLAME OUT DETECTED!", text_color="red")
        status_frame.configure(border_color="red", border_width=2)
    else:
        status_label.configure(text="✅ SYSTEM OPERATIONAL", text_color="#00FF00")
        status_frame.configure(border_color="#00FF00", border_width=2)
        
    if mute_state == "1":
        mute_btn.configure(text="🔕 ALARM MUTED", fg_color="#065397") 
    else:
        mute_btn.configure(text="🔊 BUZZER ACTIVE", fg_color="#D30000") 

    if led_state == "1":
        led_btn.configure(text="💡 LEDS ENABLED", fg_color="#228B22") 
    else:
        led_btn.configure(text="⚫ LEDS DISABLED", fg_color="#065397") 

if ser:
    threading.Thread(target=read_from_arduino, daemon=True).start()
threading.Thread(target=advance_simulated_time_and_log, daemon=True).start()

app.mainloop()