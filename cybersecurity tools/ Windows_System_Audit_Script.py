import os
import platform
import subprocess
import psutil
import winreg

def get_system_info():
    """Gather basic system information."""
    system_info = {
        "OS": platform.system(),
        "Version": platform.version(),
        "Release": platform.release(),
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Hostname": platform.node(),
    }
    return system_info

def get_installed_programs():
    """Retrieve a list of installed programs from the Windows registry."""
    installed_programs = []
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ]
    for reg_path in reg_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                sub_key_name = winreg.EnumKey(reg_key, i)
                sub_key = winreg.OpenKey(reg_key, sub_key_name)
                try:
                    program_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                    installed_programs.append(program_name)
                except FileNotFoundError:
                    continue
        except FileNotFoundError:
            continue
    return installed_programs

def get_running_processes():
    """List all currently running processes."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def get_services():
    """List all system services and their statuses."""
    services = []
    try:
        result = subprocess.run(
            ["sc", "query"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        for line in result.stdout.splitlines():
            if "SERVICE_NAME" in line or "STATE" in line:
                services.append(line.strip())
    except Exception as e:
        services.append(f"Error retrieving services: {str(e)}")
    return services

def write_to_file(filename, content):
    """Write content to a file."""
    with open(filename, 'w') as file:
        file.write(content)

def main():
    output_file = "windows_audit.txt"
    output = []

    output.append("Windows System Audit")
    output.append("=====================\n")

    # System Info
    output.append("System Information:")
    system_info = get_system_info()
    for key, value in system_info.items():
        output.append(f"{key}: {value}")
    output.append("\n")

    # Installed Programs
    output.append("Installed Programs:")
    installed_programs = get_installed_programs()
    for program in installed_programs:
        output.append(program)
    output.append("\n")

    # Running Processes
    output.append("Running Processes:")
    processes = get_running_processes()
    for process in processes:
        output.append(f"PID: {process['pid']}, Name: {process['name']}")
    output.append("\n")

    # System Services
    output.append("System Services:")
    services = get_services()
    for service in services:
        output.append(service)
    output.append("\n")

    # Combine output into a single string and write to file
    full_output = "\n".join(output)
    write_to_file(output_file, full_output)

    print(f"Audit complete. Results written to {output_file}")

if __name__ == "__main__":
    main()
