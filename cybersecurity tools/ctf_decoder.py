import tkinter as tk
from tkinter import ttk, messagebox
import base64
import codecs

# Decode functions
def decode_text():
    method = method_var.get()
    text = input_entry.get("1.0", tk.END).strip()

    try:
        if method == "ROT13":
            output = codecs.decode(text, 'rot_13')

        elif method == "Base64":
            output = base64.b64decode(text.encode()).decode()

        elif method == "Hex":
            output = bytes.fromhex(text).decode()

        elif method == "Binary":
            output = ''.join([chr(int(b, 2)) for b in text.split()])

        elif method == "Octal":
            output = ''.join([chr(int(o, 8)) for o in text.split()])

        else:
            output = "Select a decoding method."

        output_entry.delete("1.0", tk.END)
        output_entry.insert(tk.END, output)

    except Exception as e:
        messagebox.showerror("Error", f"Decoding failed!\n\n{e}")

# GUI Setup
root = tk.Tk()
root.title("🧠 Offline CTF Decoder Tool")
root.geometry("600x400")

tk.Label(root, text="Enter Encoded Text:").pack(pady=5)
input_entry = tk.Text(root, height=5, width=70)
input_entry.pack(pady=5)

tk.Label(root, text="Select Decode Method:").pack(pady=5)
method_var = tk.StringVar()
method_dropdown = ttk.Combobox(root, textvariable=method_var, state='readonly',
                               values=["ROT13", "Base64", "Hex", "Binary", "Octal"])
method_dropdown.pack(pady=5)

tk.Button(root, text="🔓 Decode", command=decode_text).pack(pady=10)

tk.Label(root, text="Decoded Output:").pack(pady=5)
output_entry = tk.Text(root, height=5, width=70)
output_entry.pack(pady=5)

root.mainloop()
