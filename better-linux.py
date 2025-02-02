import tkinter as tk
import psutil
import platform
import socket
import datetime
from tkinter import ttk  # Import ttk for notebook (tabbed interface)

class SystemInfoGUI:
    def __init__(self, master):
        self.master = master
        master.title("System Information")
        master.geometry("500x600")

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create first tab for System Info
        self.system_info_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.system_info_frame, text="System Info")

        # Create a text widget to display system info in the first tab
        self.info_text = tk.Text(self.system_info_frame, height=25, width=60, font=("Courier", 10))
        self.info_text.pack(padx=10, pady=10)

        # Create second tab labeled "Extra"
        self.extra_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.extra_frame, text="Extra")

        # Add a label to the Extra tab (placeholder content)
        self.extra_label = tk.Label(self.extra_frame, text="Extra Information Coming Soon!", font=("Courier", 12))
        self.extra_label.pack(expand=True)

        # Create an exit button
        self.exit_button = tk.Button(master, text="Exit", command=self.exit_application)
        self.exit_button.pack(pady=10)

        # Populate system information
        self.update_system_info()

    def update_system_info(self):
        # Clear previous text
        self.info_text.delete(1.0, tk.END)

        # Gather system information
        info = []
        
        # Operating System Info
        info.append(f"Operating System: {platform.system()} {platform.release()}")
        info.append(f"OS Version: {platform.version()}")
        
        # CPU Info
        cpu_count = psutil.cpu_count(logical=False)
        logical_cpu_count = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        info.append(f"CPU Cores: {cpu_count} Physical, {logical_cpu_count} Logical")
        info.append(f"CPU Frequency: {cpu_freq.current:.2f} MHz")
        
        # Memory Info
        memory = psutil.virtual_memory()
        info.append(f"Total Memory: {memory.total / (1024**3):.2f} GB")
        info.append(f"Available Memory: {memory.available / (1024**3):.2f} GB")
        info.append(f"Memory Usage: {memory.percent}%")
        
        # Disk Info
        disk = psutil.disk_usage('/')
        info.append(f"Total Disk Space: {disk.total / (1024**3):.2f} GB")
        info.append(f"Free Disk Space: {disk.free / (1024**3):.2f} GB")
        info.append(f"Disk Usage: {disk.percent}%")
        
        # Network Info
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        info.append(f"Hostname: {hostname}")
        info.append(f"IP Address: {ip_address}")
        
        # Current Time
        current_time = datetime.datetime.now()
        info.append(f"Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Insert information into text widget
        for line in info:
            self.info_text.insert(tk.END, line + "\n")

    def exit_application(self):
        # Close the application
        self.master.destroy()

def main():
    root = tk.Tk()
    system_info_gui = SystemInfoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()