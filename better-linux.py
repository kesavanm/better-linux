import tkinter as tk
import psutil
import platform
import socket
import datetime
import subprocess
import threading
import os
from tkinter import ttk, messagebox, simpledialog

# Try to import ttkbootstrap, fallback to standard ttk if not available
try:
    import ttkbootstrap as ttk_theme
    USING_TTKBOOTSTRAP = True
except ImportError:
    ttk_theme = ttk
    USING_TTKBOOTSTRAP = False
    print("ttkbootstrap not available. Falling back to standard ttk.")

class SystemInfoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Kesavan's Better Gnu/Linux !")
        master.geometry("500x600")

        # Create notebook (tabbed interface)
        self.notebook = ttk_theme.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create first tab for System Info
        self.system_info_frame = ttk_theme.Frame(self.notebook)
        self.notebook.add(self.system_info_frame, text="System Info")

        # Create a text widget to display system info in the first tab
        self.info_text = tk.Text(self.system_info_frame, height=25, width=60, font=("Courier", 10))
        self.info_text.pack(padx=10, pady=10)

        # Create second tab labeled "Extra"
        self.extra_frame = ttk_theme.Frame(self.notebook)
        self.notebook.add(self.extra_frame, text="Extra")

        # Create a Treeview widget for tools table
        self.tools_table = ttk_theme.Treeview(self.extra_frame, columns=('SNo', 'Tool', 'Version'), show='headings')
        self.tools_table.heading('SNo', text='S.No')
        self.tools_table.heading('Tool', text='Tool')
        self.tools_table.heading('Version', text='Version')
        
        # Configure column widths
        self.tools_table.column('SNo', width=50, anchor='center')
        self.tools_table.column('Tool', width=150)
        self.tools_table.column('Version', width=250)
        
        self.tools_table.pack(padx=10, pady=10, expand=True, fill='both')

        # Create third tab labeled "Additional Tools"
        self.additional_tools_frame = ttk_theme.Frame(self.notebook)
        self.notebook.add(self.additional_tools_frame, text="Additional Tools")

        # Create a Treeview widget for additional tools table
        self.additional_tools_table = ttk_theme.Treeview(self.additional_tools_frame, 
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

        # Create fourth tab labeled "Credits"
        self.credits_frame = ttk_theme.Frame(self.notebook)
        self.notebook.add(self.credits_frame, text="Credits")

        # Create a text widget for credits
        self.credits_text = tk.Text(
            self.credits_frame, 
            height=25, 
            width=60, 
            font=("Courier", 10), 
            wrap=tk.WORD
        )
        self.credits_text.pack(padx=10, pady=10, expand=True, fill='both')

        # Configure tags for hyperlinks and heart
        self.credits_text.tag_configure("hyperlink", foreground="blue", underline=True)
        self.credits_text.tag_configure("red_heart", foreground="red")
        
        # Bind hyperlink click event
        self.credits_text.tag_bind("hyperlink", "<Button-1>", self.open_link)
        self.credits_text.tag_bind("hyperlink", "<Enter>", lambda e: self.credits_text.config(cursor="hand2"))
        self.credits_text.tag_bind("hyperlink", "<Leave>", lambda e: self.credits_text.config(cursor=""))

        # Insert credits information
        credits_content = """Better Linux: System Information Tool

Author:
Kesavan Muthuvel
Personal Website: """

        self.credits_text.insert(tk.END, credits_content)
        self.credits_text.insert(tk.END, "https://kesavan.info", "hyperlink")
        
        credits_content_continued = """

About:
Better Linux is a comprehensive system information and tool management 
application designed to provide users with quick insights into their 
Linux system and easy management of additional tools.

Key Features:
- Detailed System Information
- Tool Version Checking
- One-Click Tool Installation/Uninstallation

Created """
        
        self.credits_text.insert(tk.END, credits_content_continued)
        self.credits_text.insert(tk.END, "", "red_heart")
        
        credits_content_final = """ using:
- Windsurf Editor: """
        
        self.credits_text.insert(tk.END, credits_content_final)
        self.credits_text.insert(tk.END, "https://x.com/WindsurfEditor", "hyperlink")
        
        credits_content_cascade = """
- Cascade AI Assistant: """
        
        self.credits_text.insert(tk.END, credits_content_cascade)
        self.credits_text.insert(tk.END, "https://codeium.com", "hyperlink")

        credits_content_end = """

Development Philosophy:
Simplifying Linux system management and providing 
an intuitive, user-friendly interface.

Feedback & Support:
For bugs, suggestions, or feedback, please contact:
Email: gnu@kesavan.info

Version: 1.0.0
Release Date: February 2025

Thank you for using Better Linux!
"""
        self.credits_text.insert(tk.END, credits_content_end)
        
        self.credits_text.config(state=tk.DISABLED)  # Make text read-only

        # Create fifth tab labeled "Console"
        self.console_frame = ttk_theme.Frame(self.notebook)
        self.notebook.add(self.console_frame, text="Console")

        # Create a text widget for console output
        self.console_text = tk.Text(
            self.console_frame, 
            height=25, 
            width=60, 
            font=("Courier", 10), 
            wrap=tk.WORD,
            state=tk.DISABLED  # Start in read-only mode
        )
        self.console_text.pack(padx=10, pady=10, expand=True, fill='both')

        # Create a clear button for console
        self.clear_console_button = ttk_theme.Button(
            self.console_frame, 
            text="Clear Console", 
            command=self.clear_console
        )
        self.clear_console_button.pack(pady=5)

        # Configure tags for different types of console messages
        self.console_text.tag_configure("info", foreground="blue")
        self.console_text.tag_configure("success", foreground="green")
        self.console_text.tag_configure("error", foreground="red")

        # Add a status bar that is copyable
        self.status_var = tk.StringVar()
        self.status_bar = ttk_theme.Entry(
            master, 
            textvariable=self.status_var, 
            state='readonly',  # Make it read-only but copyable
            font=("Courier", 10)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Create a frame for buttons
        self.additional_tools_button_frame = ttk_theme.Frame(self.additional_tools_frame)
        self.additional_tools_button_frame.pack(pady=10)

        # Refresh button
        self.refresh_button = ttk_theme.Button(
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
        # Restore full list of additional tools to check
        additional_tools = [
            {'name': 'cowsay', 'description': 'Generates an ASCII picture of a cow with a message', 'package': 'cowsay'},
            {'name': 'fortune', 'description': 'Prints a random, hopefully interesting, adage', 'package': 'fortune-mod'},
            {'name': 'lolcat', 'description': 'Outputs text in rainbow colors', 'package': 'lolcat'},
            {'name': 'duf', 'description': 'Disk Usage/Free utility with a nice UI', 'package': 'duf'},
            {'name': 'bat', 'description': 'A cat clone with syntax highlighting', 'package': 'bat'},
            {'name': 'ncdu', 'description': 'NCurses Disk Usage', 'package': 'ncdu'},
            {'name': 'htop', 'description': 'Interactive process viewer', 'package': 'htop'},
            {'name': 'sl', 'description': 'Steam Locomotive animation', 'package': 'sl'},
            {'name': 'toilet', 'description': 'Prints text using large letters', 'package': 'toilet'},
            {'name': 'sysvbanner', 'description': 'Print large banner messages', 'package': 'sysvbanner'},
            {'name': 'figlet', 'description': 'Create large text banners', 'package': 'figlet'},
            {'name': 'boxes', 'description': 'Draw ASCII art boxes around text', 'package': 'boxes'},
            {'name': 'autoconf', 'description': 'Generates configuration scripts', 'package': 'autoconf'},
            {'name': 'build-essential', 'description': 'Compilation tools', 'package': 'build-essential'},
            {'name': 'curl', 'description': 'Transfer data from or to a server', 'package': 'curl'},
            {'name': 'wget', 'description': 'Retrieve files using HTTP, HTTPS, and FTP', 'package': 'wget'},
            {'name': 'dos2unix', 'description': 'Convert text between DOS and Unix formats', 'package': 'dos2unix'},
            {'name': 'gcc', 'description': 'GNU Compiler Collection', 'package': 'gcc'},
            {'name': 'git', 'description': 'Distributed version control system', 'package': 'git'},
            {'name': 'libncurses-dev', 'description': 'Developer libraries for ncurses', 'package': 'libncurses-dev'},
            {'name': 'make', 'description': 'Build automation tool', 'package': 'make'},
            {'name': 'x11-xserver-utils', 'description': 'X11 utilities', 'package': 'x11-xserver-utils'},
            {'name': 'net-tools', 'description': 'Network configuration tools', 'package': 'net-tools'},
            {'name': 'ffmpeg', 'description': 'Multimedia framework', 'package': 'ffmpeg'}
        ]

        # Populate the table
        for index, tool in enumerate(additional_tools, 1):
            installed = self.is_tool_installed(tool['name'])
            version = self.get_tool_version(tool['name']) if installed == 'Yes' else 'N/A'
            
            # Determine button text based on installation status
            install_text = 'Install' if installed == 'No' else ''
            uninstall_text = 'Uninstall' if installed == 'Yes' else ''
            
            self.additional_tools_table.insert('', 'end', values=(
                index, 
                tool['name'], 
                installed, 
                version, 
                install_text, 
                uninstall_text
            ), tags=(tool['name'],))
        
        # Bind click events to handle installation/uninstallation
        self.additional_tools_table.bind('<Button-1>', self.on_tool_table_click)

    def on_tool_table_click(self, event):
        # Get the row that was clicked
        region = self.additional_tools_table.identify("region", event.x, event.y)
        if region != "cell":
            return

        # Get the row and column
        row = self.additional_tools_table.identify_row(event.y)
        column = self.additional_tools_table.identify_column(event.x)

        if not row:
            return

        # Get the values of the clicked row
        values = self.additional_tools_table.item(row, 'values')
        
        # Find the corresponding tool
        tool_name = values[1]
        tool = next((t for t in [
            {'name': 'cowsay', 'description': 'Generates an ASCII picture of a cow with a message', 'package': 'cowsay'},
            {'name': 'fortune', 'description': 'Prints a random, hopefully interesting, adage', 'package': 'fortune-mod'},
            {'name': 'lolcat', 'description': 'Outputs text in rainbow colors', 'package': 'lolcat'},
            {'name': 'duf', 'description': 'Disk Usage/Free utility with a nice UI', 'package': 'duf'},
            {'name': 'bat', 'description': 'A cat clone with syntax highlighting', 'package': 'bat'},
            {'name': 'ncdu', 'description': 'NCurses Disk Usage', 'package': 'ncdu'},
            {'name': 'htop', 'description': 'Interactive process viewer', 'package': 'htop'},
            {'name': 'sl', 'description': 'Steam Locomotive animation', 'package': 'sl'},
            {'name': 'toilet', 'description': 'Prints text using large letters', 'package': 'toilet'},
            {'name': 'sysvbanner', 'description': 'Print large banner messages', 'package': 'sysvbanner'},
            {'name': 'figlet', 'description': 'Create large text banners', 'package': 'figlet'},
            {'name': 'boxes', 'description': 'Draw ASCII art boxes around text', 'package': 'boxes'},
            {'name': 'autoconf', 'description': 'Generates configuration scripts', 'package': 'autoconf'},
            {'name': 'build-essential', 'description': 'Compilation tools', 'package': 'build-essential'},
            {'name': 'curl', 'description': 'Transfer data from or to a server', 'package': 'curl'},
            {'name': 'wget', 'description': 'Retrieve files using HTTP, HTTPS, and FTP', 'package': 'wget'},
            {'name': 'dos2unix', 'description': 'Convert text between DOS and Unix formats', 'package': 'dos2unix'},
            {'name': 'gcc', 'description': 'GNU Compiler Collection', 'package': 'gcc'},
            {'name': 'git', 'description': 'Distributed version control system', 'package': 'git'},
            {'name': 'libncurses-dev', 'description': 'Developer libraries for ncurses', 'package': 'libncurses-dev'},
            {'name': 'make', 'description': 'Build automation tool', 'package': 'make'},
            {'name': 'x11-xserver-utils', 'description': 'X11 utilities', 'package': 'x11-xserver-utils'},
            {'name': 'net-tools', 'description': 'Network configuration tools', 'package': 'net-tools'},
            {'name': 'ffmpeg', 'description': 'Multimedia framework', 'package': 'ffmpeg'}
        ] if t['name'] == tool_name), None)

        if not tool:
            return

        # Check which column was clicked (Install or Uninstall)
        if column == '#5' and values[4] == 'Install':
            # Install tool
            self.install_tool(tool)
        elif column == '#6' and values[5] == 'Uninstall':
            # Uninstall tool
            self.uninstall_tool(tool)

    def is_tool_installed(self, tool):
        try:
            # Multiple methods to check tool installation
            def check_which(t):
                try:
                    result = subprocess.run(['which', t], 
                                            capture_output=True, 
                                            text=True, 
                                            timeout=2)
                    return result.returncode == 0
                except Exception:
                    return False

            def check_dpkg(t):
                try:
                    result = subprocess.run(['dpkg', '-s', t], 
                                            capture_output=True, 
                                            text=True, 
                                            timeout=2)
                    # Check return code and output
                    if result.returncode == 0:
                        return True
                    
                    # Check for specific dpkg messages
                    error_messages = [
                        'package is not installed',
                        'no information available',
                        'not installed and no information is available'
                    ]
                    return not any(msg in (result.stderr.lower() + result.stdout.lower()) for msg in error_messages)
                except Exception:
                    return False

            def check_dpkg_query(t):
                try:
                    result = subprocess.run(['dpkg-query', '-W', '-f=${Status}', t], 
                                            capture_output=True, 
                                            text=True, 
                                            timeout=2)
                    # Check if package is installed (looking for 'install ok installed')
                    return 'install ok installed' in result.stdout.lower()
                except Exception:
                    return False

            def check_apt_cache(t):
                try:
                    result = subprocess.run(['apt-cache', 'policy', t], 
                                            capture_output=True, 
                                            text=True, 
                                            timeout=2)
                    # Check if package is found in repositories
                    return '***' not in result.stdout and 'none' not in result.stdout.lower()
                except Exception:
                    return False

            def check_file_exists(t):
                return (os.path.exists(f'/usr/bin/{t}') or 
                        os.path.exists(f'/usr/local/bin/{t}') or 
                        os.path.exists(f'/usr/sbin/{t}') or
                        os.path.exists(f'/bin/{t}'))

            # Special cases for specific tools
            special_cases = {
                'bat': [
                    lambda: os.path.exists('/usr/bin/batcat'),  # Ubuntu/Debian specific symlink
                    lambda: subprocess.run(['batcat', '--version'], 
                                           capture_output=True, 
                                           text=True, 
                                           timeout=2).returncode == 0
                ]
            }

            # Check special cases first
            if tool in special_cases:
                for check in special_cases[tool]:
                    if check():
                        return 'Yes'

            # Comprehensive installation checks
            installation_checks = [
                check_which,
                check_dpkg,
                check_dpkg_query,
                check_file_exists
            ]

            # Track successful checks
            successful_checks = 0
            total_checks = len(installation_checks)

            # Try standard installation checks
            for check in installation_checks:
                try:
                    if check(tool):
                        successful_checks += 1
                except Exception:
                    continue

            # Determine installation status
            # Require at least 2 successful checks to confirm installation
            if successful_checks >= 2:
                return 'Yes'
            elif successful_checks == 1:
                # If only one check passes, do an additional apt-cache check
                return 'Yes' if check_apt_cache(tool) else 'No'
            else:
                return 'No'

        except Exception as e:
            # Log the error and return unknown
            self.log_to_console(f"Error checking {tool} installation: {str(e)}", "error")
            return 'No'

    def get_tool_version(self, tool):
        try:
            # Comprehensive version retrieval methods
            version_commands = {
                'cowsay': [
                    ['cowsay', '-h'],
                    ['cowsay', '--version'],
                    ['dpkg', '-s', 'cowsay']
                ],
                'fortune': [
                    ['fortune', '-V'],
                    ['fortune', '--version'],
                    ['dpkg', '-s', 'fortune-mod']
                ],
                'lolcat': [
                    ['lolcat', '--version'],
                    ['gem', 'list', 'lolcat']
                ],
                'duf': [
                    ['duf', '--version'],
                    ['dpkg', '-s', 'duf']
                ],
                'bat': [
                    ['bat', '--version'],
                    ['dpkg', '-s', 'bat']
                ],
                'ncdu': [
                    ['ncdu', '-v'],
                    ['ncdu', '--version'],
                    ['dpkg', '-s', 'ncdu']
                ],
                'htop': [
                    ['htop', '--version'],
                    ['dpkg', '-s', 'htop']
                ],
                'sl': [
                    ['dpkg', '-s', 'sl'],
                    ['apt-cache', 'policy', 'sl'],
                    ['ls', '-l', '/usr/bin/sl']
                ],
                'toilet': [
                    ['toilet', '--version'],
                    ['dpkg', '-s', 'toilet']
                ],
                'figlet': [
                    ['figlet', '-v'],
                    ['figlet', '--version'],
                    ['dpkg', '-s', 'figlet']
                ],
                'boxes': [
                    ['boxes', '-v'],
                    ['dpkg', '-s', 'boxes']
                ],
                'git': [
                    ['git', '--version'],
                    ['dpkg', '-s', 'git']
                ]
            }
            
            # Get list of commands to try for this tool
            commands = version_commands.get(tool, [
                [tool, '--version'], 
                [tool, '-v'], 
                ['dpkg', '-s', tool],
                ['apt-cache', 'policy', tool]
            ])
            
            for cmd in commands:
                try:
                    result = subprocess.run(
                        cmd, 
                        capture_output=True, 
                        text=True, 
                        timeout=2
                    )
                    
                    # Different parsing for different command types
                    if cmd[0] == 'dpkg':
                        # Look for Version line in dpkg output
                        for line in result.stdout.split('\n'):
                            if line.startswith('Version:'):
                                return line.split(':', 1)[1].strip()
                    
                    if cmd[0] == 'apt-cache':
                        # Look for Installed line in apt-cache output
                        for line in result.stdout.split('\n'):
                            if 'Installed:' in line:
                                return line.split(':', 1)[1].strip()
                    
                    # Extract version from output
                    version_line = result.stdout.strip() or result.stderr.strip()
                    
                    # Remove common prefixes and clean up version string
                    for prefix in ['version', 'Version', 'v', 'V']:
                        if version_line.lower().startswith(prefix.lower()):
                            version_line = version_line[len(prefix):].strip()
                    
                    # Additional cleanup
                    version_line = version_line.split('\n')[0].strip()
                    
                    # Return version if not empty
                    if version_line and version_line.lower() not in ['', 'none']:
                        return version_line
                
                except subprocess.TimeoutExpired:
                    # If this specific command times out, try next
                    continue
                except Exception:
                    # Silently continue to next method
                    continue
            
            # If no version found
            return 'N/A'
        
        except Exception as e:
            self.log_to_console(f"Error getting {tool} version: {str(e)}", "error")
            return 'N/A'

    def install_tool(self, tool):
        def install_thread():
            try:
                status_message = f"Installing {tool['name']}..."
                self.update_status(status_message)
                self.log_to_console(status_message)

                # Run installation command
                result = subprocess.run(
                    ['sudo', 'apt-get', 'install', '-y', tool['package']], 
                    capture_output=True, 
                    text=True
                )
                
                # Log stdout and stderr
                if result.stdout:
                    self.log_to_console(f"STDOUT: {result.stdout}", "info")
                if result.stderr:
                    self.log_to_console(f"STDERR: {result.stderr}", "error")

                # Check installation status
                if result.returncode == 0:
                    success_message = f"{tool['name']} installed successfully!"
                    self.update_status(success_message)
                    self.log_to_console(success_message, "success")
                else:
                    error_message = f"Error installing {tool['name']}"
                    self.update_status(error_message)
                    self.log_to_console(error_message, "error")
                
                # Refresh the table
                self.master.after(0, self.refresh_additional_tools)
            except Exception as e:
                error_message = f"Installation error: {str(e)}"
                self.update_status(error_message)
                self.log_to_console(error_message, "error")

        threading.Thread(target=install_thread, daemon=True).start()

    def uninstall_tool(self, tool):
        def uninstall_thread():
            try:
                status_message = f"Uninstalling {tool['name']}..."
                self.update_status(status_message)
                self.log_to_console(status_message)

                # Run uninstallation command
                result = subprocess.run(
                    ['sudo', 'apt-get', 'remove', '-y', tool['package']], 
                    capture_output=True, 
                    text=True
                )
                
                # Log stdout and stderr
                if result.stdout:
                    self.log_to_console(f"STDOUT: {result.stdout}", "info")
                if result.stderr:
                    self.log_to_console(f"STDERR: {result.stderr}", "error")

                # Check uninstallation status
                if result.returncode == 0:
                    success_message = f"{tool['name']} uninstalled successfully!"
                    self.update_status(success_message)
                    self.log_to_console(success_message, "success")
                else:
                    error_message = f"Error uninstalling {tool['name']}"
                    self.update_status(error_message)
                    self.log_to_console(error_message, "error")
                
                # Refresh the table
                self.master.after(0, self.refresh_additional_tools)
            except Exception as e:
                error_message = f"Uninstallation error: {str(e)}"
                self.update_status(error_message)
                self.log_to_console(error_message, "error")

        threading.Thread(target=uninstall_thread, daemon=True).start()

    def update_status(self, message):
        # Truncate message if it's too long to prevent UI stretching
        max_length = 120
        if len(message) > max_length:
            message = message[:max_length] + "..."
        
        self.status_var.set(message)
        self.master.update_idletasks()

    def refresh_additional_tools(self):
        # Clear existing table
        for item in self.additional_tools_table.get_children():
            self.additional_tools_table.delete(item)
        
        # Populate the table with updated tool information
        self.populate_additional_tools_table()
        
        # Log the refresh action
        self.log_to_console("Refreshed additional tools list", "info")
        
        # Update status
        self.update_status("Tools list refreshed successfully")

    def log_to_console(self, message, tag="info"):
        # Enable text widget for editing
        self.console_text.config(state=tk.NORMAL)
        
        # Add timestamp to message
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}\n"
        
        # Insert message with appropriate tag
        self.console_text.insert(tk.END, full_message, tag)
        
        # Scroll to the end
        self.console_text.see(tk.END)
        
        # Disable text widget
        self.console_text.config(state=tk.DISABLED)

    def clear_console(self):
        # Enable text widget for editing
        self.console_text.config(state=tk.NORMAL)
        
        # Clear all text
        self.console_text.delete(1.0, tk.END)
        
        # Disable text widget
        self.console_text.config(state=tk.DISABLED)

    def exit_application(self):
        # Close the application
        self.master.destroy()

    def open_link(self, event):
        # Get the index of the clicked position
        index = self.credits_text.index(f"@{event.x},{event.y}")
        
        # Get the tags at this index
        tags = self.credits_text.tag_names(index)
        
        # Check if hyperlink tag is present
        if "hyperlink" in tags:
            # Get the text of the hyperlink
            start = self.credits_text.index(f"{index} linestart")
            end = self.credits_text.index(f"{index} lineend")
            line_text = self.credits_text.get(start, end)
            
            # Extract URL (assumes URL is the last part of the line)
            url = line_text.split(": ")[-1].strip()
            
            # Open the URL in default browser
            import webbrowser
            webbrowser.open(url)

def main():
    root = tk.Tk()
    system_info_gui = SystemInfoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()