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
        self.tools_table = ttk.Treeview(self.extra_frame, columns=('SNo', 'Tool', 'Version'), show='headings')
        self.tools_table.heading('SNo', text='S.No')
        self.tools_table.heading('Tool', text='Tool')
        self.tools_table.heading('Version', text='Version')
        
        # Configure column widths
        self.tools_table.column('SNo', width=50, anchor='center')
        self.tools_table.column('Tool', width=150)
        self.tools_table.column('Version', width=250)
        
        self.tools_table.pack(padx=10, pady=10, expand=True, fill='both')

        # Create third tab labeled "Additional Tools"
        self.additional_tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.additional_tools_frame, text="Additional Tools")

        # Create a Treeview widget for additional tools table
        self.additional_tools_table = ttk.Treeview(self.additional_tools_frame, 
                                                   columns=('SNo', 'Tool', 'Installed', 'Version', 'Install', 'Uninstall'), 
                                                   show='headings')
        self.additional_tools_table.heading('SNo', text='S.No')
        self.additional_tools_table.heading('Tool', text='Tool')
        self.additional_tools_table.heading('Installed', text='Installed')
        self.additional_tools_table.heading('Version', text='Version')
        self.additional_tools_table.heading('Install', text='Install')
        self.additional_tools_table.heading('Uninstall', text='Uninstall')
        
        # Configure column widths
        self.additional_tools_table.column('SNo', width=50, anchor='center')
        self.additional_tools_table.column('Tool', width=100)
        self.additional_tools_table.column('Installed', width=80)
        self.additional_tools_table.column('Version', width=100)
        self.additional_tools_table.column('Install', width=75)
        self.additional_tools_table.column('Uninstall', width=75)
        
        self.additional_tools_table.pack(padx=10, pady=10, expand=True, fill='both')

        # Create a frame for buttons
        self.additional_tools_button_frame = ttk.Frame(self.additional_tools_frame)
        self.additional_tools_button_frame.pack(pady=10)

        # Refresh button
        self.refresh_button = ttk.Button(
            self.additional_tools_button_frame, 
            text="Refresh Tools List", 
            command=self.refresh_additional_tools
        )
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        # Populate tools table
        self.populate_tools_table()

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
        for index, tool in enumerate(tools_to_check, 1):
            version = get_tool_version(tool)
            self.tools_table.insert('', 'end', values=(index, tool, version))

    def populate_additional_tools_table(self):
        # List of additional tools to check
        additional_tools = [
            'cowsay', 'fortune', 'lolcat', 'duf', 'bat', 'ncdu', 'htop', 'sl', 
            'toilet', 'sysvbanner', 'figlet', 'boxes', 'autoconf', 'build-essential', 
            'curl', 'wget', 'dos2unix', 'gcc', 'git', 'libncurses-dev', 'make', 
            'x11-xserver-utils', 'net-tools', 'ffmpeg'
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
        for index, tool in enumerate(additional_tools, 1):
            installed = is_tool_installed(tool)
            version = get_tool_version(tool) if installed == 'Yes' else 'N/A'
            
            # Insert row with install/uninstall buttons
            item = self.additional_tools_table.insert('', 'end', values=(
                index,
                tool, 
                installed, 
                version, 
                'Install' if installed == 'No' else '', 
                'Uninstall' if installed == 'Yes' else ''
            ))
            
            # Create buttons for each row
            install_button = ttk.Button(
                self.additional_tools_table, 
                text='Install', 
                command=lambda t=tool: self.toggle_tool_installation(t, 'install')
            )
            
            uninstall_button = ttk.Button(
                self.additional_tools_table, 
                text='Uninstall', 
                command=lambda t=tool: self.toggle_tool_installation(t, 'uninstall')
            )
            
            # Add buttons to the table
            self.additional_tools_table.item(item, tags=(item,))
            
            # Bind events for dynamic button placement
            self.additional_tools_table.tag_bind(item, '<Button-1>', 
                                                 lambda event, 
                                                 install_btn=install_button, 
                                                 uninstall_btn=uninstall_button: 
                                                 self.show_button(event, install_btn, uninstall_btn))

    def show_button(self, event, install_button, uninstall_button):
        # Get the item under the mouse
        item = self.additional_tools_table.identify_row(event.y)
        column = self.additional_tools_table.identify_column(event.x)
        
        if not item:
            return

        # Get the bounding rectangle for the 'Install' or 'Uninstall' column
        x, y, width, height = self.additional_tools_table.bbox(item, column)
        
        # Position and show the appropriate button
        if column == '#5':  # Install column
            install_button.place(x=x, y=y, width=width, height=height)
            uninstall_button.place_forget()
        elif column == '#6':  # Uninstall column
            uninstall_button.place(x=x, y=y, width=width, height=height)
            install_button.place_forget()
        else:
            install_button.place_forget()
            uninstall_button.place_forget()

    def toggle_tool_installation(self, tool, action):
        # Prepare installation/uninstallation commands
        install_commands = {
            'cowsay': ('sudo apt-get install -y cowsay', 'sudo apt-get remove -y cowsay'),
            'fortune': ('sudo apt-get install -y fortune-mod', 'sudo apt-get remove -y fortune-mod'),
            'lolcat': ('sudo gem install lolcat', 'sudo gem uninstall -y lolcat'),
            'duf': (
                'wget https://github.com/muesli/duf/releases/download/v0.8.1/duf_0.8.1_linux_amd64.deb && sudo dpkg -i duf_0.8.1_linux_amd64.deb',
                'sudo dpkg -r duf'
            ),
            # Add more tools with their install/uninstall commands
            'bat': ('sudo apt-get install -y bat', 'sudo apt-get remove -y bat'),
            'ncdu': ('sudo apt-get install -y ncdu', 'sudo apt-get remove -y ncdu'),
            'htop': ('sudo apt-get install -y htop', 'sudo apt-get remove -y htop'),
            'sl': ('sudo apt-get install -y sl', 'sudo apt-get remove -y sl'),
            'toilet': ('sudo apt-get install -y toilet', 'sudo apt-get remove -y toilet'),
            'sysvbanner': ('sudo apt-get install -y sysvbanner', 'sudo apt-get remove -y sysvbanner'),
            'figlet': ('sudo apt-get install -y figlet', 'sudo apt-get remove -y figlet'),
            'boxes': ('sudo apt-get install -y boxes', 'sudo apt-get remove -y boxes'),
        }

        try:
            # Choose the appropriate command based on action
            command = install_commands.get(tool, (None, None))
            
            if action == 'install':
                # Install
                subprocess.run(command[0], shell=True, check=True)
                action_text = "installed"
            else:
                # Uninstall
                subprocess.run(command[1], shell=True, check=True)
                action_text = "uninstalled"
            
            # Refresh the table
            self.additional_tools_table.delete(*self.additional_tools_table.get_children())
            self.populate_additional_tools_table()
            
            messagebox.showinfo("Success", f"{tool} {action_text} successfully!")
        
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", f"Failed to {action} {tool}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_additional_tools(self):
        try:
            # Clear the current table
            self.additional_tools_table.delete(*self.additional_tools_table.get_children())
            
            # Repopulate the table
            self.populate_additional_tools_table()
            
            # Show a success message
            messagebox.showinfo("Refresh", "Tools list updated successfully!")
        
        except Exception as e:
            messagebox.showerror("Refresh Error", f"Failed to refresh tools list: {str(e)}")

    def exit_application(self):
        # Close the application
        self.master.destroy()

def main():
    root = tk.Tk()
    system_info_gui = SystemInfoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()