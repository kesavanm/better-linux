import tkinter as tk
import psutil
import platform
import socket
import datetime
import subprocess
from tkinter import ttk, messagebox  # Import ttk for notebook (tabbed interface)

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

        # Remove the placeholder label
        self.extra_label.destroy()

        # Create a Treeview widget for tools table
        self.tools_table = ttk.Treeview(self.extra_frame, columns=('Tool', 'Version'), show='headings')
        self.tools_table.heading('Tool', text='Tool')
        self.tools_table.heading('Version', text='Version')
        self.tools_table.pack(padx=10, pady=10, expand=True, fill='both')

        # Populate tools table
        self.populate_tools_table()

        # Create third tab labeled "Additional Tools"
        self.additional_tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.additional_tools_frame, text="Additional Tools")

        # Create a Treeview widget for additional tools table
        self.additional_tools_table = ttk.Treeview(self.additional_tools_frame, 
                                                   columns=('Tool', 'Installed', 'Version'), 
                                                   show='headings')
        self.additional_tools_table.heading('Tool', text='Tool')
        self.additional_tools_table.heading('Installed', text='Installed')
        self.additional_tools_table.heading('Version', text='Version')
        self.additional_tools_table.pack(padx=10, pady=10, expand=True, fill='both')

        # Create frame for buttons
        self.additional_tools_button_frame = ttk.Frame(self.additional_tools_frame)
        self.additional_tools_button_frame.pack(pady=10)

        # Install button
        self.install_button = ttk.Button(self.additional_tools_button_frame, 
                                         text="Install Selected Tool", 
                                         command=self.install_selected_tool)
        self.install_button.pack(side=tk.LEFT, padx=5)

        # Version Info button
        self.version_button = ttk.Button(self.additional_tools_button_frame, 
                                         text="Show Version", 
                                         command=self.show_tool_version)
        self.version_button.pack(side=tk.LEFT, padx=5)

        # Populate additional tools table
        self.populate_additional_tools_table()

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

    def populate_tools_table(self):
        # List of common Linux tools to check
        tools_to_check = [
            'cat', 'ls', 'cut', 'grep', 'sed', 'awk', 
            'find', 'tar', 'gzip', 'zip', 'unzip', 
            'curl', 'wget', 'ssh', 'scp'
        ]

        # Function to get tool version
        def get_tool_version(tool):
            try:
                result = subprocess.run([tool, '--version'], 
                                        capture_output=True, 
                                        text=True, 
                                        timeout=2)
                # Extract first line of version output
                version = result.stdout.split('\n')[0].strip()
                return version
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                return 'N/A'

        # Populate the table
        for tool in tools_to_check:
            version = get_tool_version(tool)
            self.tools_table.insert('', 'end', values=(tool, version))

    def populate_additional_tools_table(self):
        # List of additional tools to check

	# # tools
	# sudo apt install autoconf build-essential curl wget dos2unix gcc git
	# sudo apt install libncurses-dev make
	# sudo apt install make-guile x11-xserver-utils net-tools

	# # media
	# sudo apt install ffmpeg

	# # funtime
	# sudo apt install bat cowsay fortune lolcat sl
	# sudo apt install toilet sysvbanner figlet boxes

	# # extra
	# sudo apt install ncdu





        additional_tools = [
            'cowsay', 'fortune', 'lolcat', 'duf' , 'bat' , 'ncdu', 'htop', 'sl', 'toilet', 'sysvbanner', 'figlet', 'boxes',
            'autoconf', 'build-essential', 'curl', 'wget', 'dos2unix', 'gcc', 'git', 'libncurses-dev', 'make', 'x11-xserver-utils', 'net-tools',
            'ffmpeg',
            'bat', 'cowsay', 'fortune', 'lolcat', 'sl',
            'toilet', 'sysvbanner', 'figlet', 'boxes',
            'ncdu'
        ]

        # Function to check if tool is installed
        def is_tool_installed(tool):
            try:
                subprocess.run(['which', tool], 
                               capture_output=True, 
                               text=True, 
                               check=True)
                return 'Yes'
            except subprocess.CalledProcessError:
                return 'No'

        # Function to get tool version
        def get_tool_version(tool):
            try:
                if tool == 'cowsay':
                    result = subprocess.run(['cowsay', '-h'], 
                                            capture_output=True, 
                                            text=True, 
                                            timeout=2)
                    # Extract version from help text
                    version_lines = [line for line in result.stderr.split('\n') if 'version' in line.lower()]
                    return version_lines[0] if version_lines else 'N/A'
                elif tool == 'fortune':
                    result = subprocess.run(['fortune', '-v'], 
                                            capture_output=True, 
                                            text=True, 
                                            timeout=2)
                    return result.stderr.strip()
                elif tool == 'lolcat':
                    result = subprocess.run(['lolcat', '--version'], 
                                            capture_output=True, 
                                            text=True, 
                                            timeout=2)
                    return result.stdout.strip()
                elif tool == 'duf':
                    result = subprocess.run(['duf', '--version'], 
                                            capture_output=True, 
                                            text=True, 
                                            timeout=2)
                    return result.stdout.strip()
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired, IndexError):
                return 'N/A'

        # Populate the table
        for tool in additional_tools:
            installed = is_tool_installed(tool)
            version = get_tool_version(tool) if installed == 'Yes' else 'N/A'
            self.additional_tools_table.insert('', 'end', values=(tool, installed, version))

    def install_selected_tool(self):
        # Get the selected tool
        selected_item = self.additional_tools_table.selection()
        if not selected_item:
            tk.messagebox.showwarning("Warning", "Please select a tool to install")
            return

        # Get the tool name
        tool = self.additional_tools_table.item(selected_item)['values'][0]

        # Prepare installation command based on the tool
        install_commands = {
            'cowsay': 'sudo apt-get install -y cowsay',
            'fortune': 'sudo apt-get install -y fortune-mod',
            'lolcat': 'sudo gem install lolcat',
            'duf': 'wget https://github.com/muesli/duf/releases/download/v0.8.1/duf_0.8.1_linux_amd64.deb && sudo dpkg -i duf_0.8.1_linux_amd64.deb'
        }

        try:
            # Run the installation command
            subprocess.run(install_commands[tool], shell=True, check=True)
            
            # Refresh the table after installation
            self.additional_tools_table.delete(*self.additional_tools_table.get_children())
            self.populate_additional_tools_table()
            
            tk.messagebox.showinfo("Success", f"{tool} installed successfully!")
        except subprocess.CalledProcessError:
            tk.messagebox.showerror("Error", f"Failed to install {tool}")

    def show_tool_version(self):
        # Get the selected tool
        selected_item = self.additional_tools_table.selection()
        if not selected_item:
            tk.messagebox.showwarning("Warning", "Please select a tool")
            return

        # Get the tool name and current version
        tool, installed, version = self.additional_tools_table.item(selected_item)['values']
        
        if installed == 'No':
            tk.messagebox.showinfo("Version Info", f"{tool} is not installed")
        else:
            tk.messagebox.showinfo("Version Info", f"{tool} version: {version}")

    def exit_application(self):
        # Close the application
        self.master.destroy()

def main():
    root = tk.Tk()
    system_info_gui = SystemInfoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()