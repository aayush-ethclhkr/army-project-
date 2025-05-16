import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import hashlib
import json

HASH_DB = "hashes.json"

def hash_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def scan_folder(folder_path):
    file_hashes = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_hash = hash_file(full_path)
            if file_hash:
                file_hashes[full_path] = file_hash
    return file_hashes

def save_hashes(hashes):
    with open(HASH_DB, 'w') as f:
        json.dump(hashes, f, indent=4)

def load_hashes():
    try:
        with open(HASH_DB, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def compare_hashes(old, new):
    results = []
    
    for file in new:
        if file not in old:
            results.append(f"[+] New file added: {file}")
        elif new[file] != old[file]:
            results.append(f"[!] File modified: {file}")
    
    for file in old:
        if file not in new:
            results.append(f"[-] File deleted: {file}")

    return results or ["[✓] No changes detected."]

# GUI Starts Here
def select_folder():
    folder = filedialog.askdirectory()
    folder_path.set(folder)

def run_check():
    folder = folder_path.get()
    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder path!")
        return
    
    new_hashes = scan_folder(folder)
    old_hashes = load_hashes()

    result_box.delete('1.0', tk.END)

    if old_hashes is None:
        result_box.insert(tk.END, "[*] No previous hash database found.\n[*] Saving current state...\n")
        save_hashes(new_hashes)
        result_box.insert(tk.END, "[✓] Hashes saved!\n")
    else:
        result_box.insert(tk.END, "=== Integrity Report ===\n\n")
        comparison = compare_hashes(old_hashes, new_hashes)
        for line in comparison:
            result_box.insert(tk.END, line + "\n")
        save_hashes(new_hashes)

# GUI Layout
root = tk.Tk()
root.title("🛡️ File Integrity Checker (GUI) - By Hacker Bhai")
root.geometry("700x500")

folder_path = tk.StringVar()

tk.Label(root, text="Select Folder to Scan:", font=("Arial", 12)).pack(pady=10)
tk.Entry(root, textvariable=folder_path, width=60).pack()
tk.Button(root, text="Browse", command=select_folder).pack(pady=5)
tk.Button(root, text="Run Integrity Check", command=run_check, bg="#007acc", fg="white").pack(pady=10)

result_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Consolas", 10))
result_box.pack(padx=10, pady=10)

root.mainloop()
