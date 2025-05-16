import tkinter as tk
from tkinter import messagebox
import base64
import random
import string
import binascii
import codecs

def generate_flag():
    return f"flag{{{''.join(random.choices(string.ascii_lowercase + string.digits, k=12))}}}"

def base64_x3_encode(data):
    encoded = data.encode()
    for _ in range(3):
        encoded = base64.b64encode(encoded)
    return encoded.decode()

def rot13_encode(data):
    return codecs.encode(data, 'rot_13')

def hex_encode(data):
    return binascii.hexlify(data.encode()).decode()

def binary_encode(data):
    return ' '.join(format(ord(char), '08b') for char in data)

def octal_encode(data):
    return ' '.join(format(ord(char), 'o') for char in data)


class CTFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Offline CTF Challenge Generator (Multi-Encoding)")
        self.flag = ""
        self.challenge = ""
        self.encoding_type = ""

   
        tk.Label(root, text="Generated Challenge:", font=("Arial", 12)).pack(pady=5)
        self.challenge_box = tk.Text(root, height=5, width=60, wrap=tk.WORD, font=("Courier", 10))
        self.challenge_box.pack(padx=10)

        tk.Button(root, text="🔁 Generate New Challenge", command=self.generate_challenge, bg="#4CAF50", fg="white").pack(pady=10)

        tk.Label(root, text="🔍 Your Decoded Flag:", font=("Arial", 12)).pack(pady=5)
        self.flag_entry = tk.Entry(root, width=40, font=("Courier", 10))
        self.flag_entry.pack(pady=5)

        tk.Button(root, text="✅ Submit Flag", command=self.verify_flag, bg="#2196F3", fg="white").pack(pady=10)

    def generate_challenge(self):
        self.flag = generate_flag()
        self.encoding_type = random.choice(['base64', 'rot13', 'hex', 'binary', 'octal'])

        if self.encoding_type == 'base64':
            self.challenge = base64_x3_encode(self.flag)
            hint = "Hint: Base64 encoded 3 times."
        elif self.encoding_type == 'rot13':
            self.challenge = rot13_encode(self.flag)
            hint = "Hint: ROT13 cipher used."
        elif self.encoding_type == 'hex':
            self.challenge = hex_encode(self.flag)
            hint = "Hint: Hexadecimal encoding."
        elif self.encoding_type == 'binary':
            self.challenge = binary_encode(self.flag)
            hint = "Hint: Binary encoding (8-bit per char)."
        elif self.encoding_type == 'octal':
            self.challenge = octal_encode(self.flag)
            hint = "Hint: Octal encoding."

        self.challenge_box.delete(1.0, tk.END)
        self.challenge_box.insert(tk.END, self.challenge)
        messagebox.showinfo("🧩 New Challenge", f"Encoding Type: {self.encoding_type.upper()}\n{hint}")

    def verify_flag(self):
        user_input = self.flag_entry.get().strip()
        if user_input == self.flag:
            messagebox.showinfo("🎉 Correct!", "Perfect! You decoded it right!")
        else:
            messagebox.showerror("❌ Wrong!", "Hmm... that's not the correct flag.")



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x450")
    app = CTFApp(root)
    root.mainloop()
