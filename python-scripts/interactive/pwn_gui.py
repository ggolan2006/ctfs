import json
import threading
from tkinter import *
from pwn import *

# Load config
with open("config.json") as f:
    CONFIG = json.load(f)

# pwntools setup
context.log_level = 'error'  # suppress noisy logging


class PwnGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Pwnable Shell - {CONFIG['challenge_name']}")

        self.text = Text(root, bg="black", fg="lime", insertbackground="white")
        self.text.pack(fill=BOTH, expand=True)

        self.entry = Entry(root, bg="black", fg="white", insertbackground="white")
        self.entry.pack(fill=X)
        self.entry.bind("<Return>", self.send_input)

        self.ssh = None
        self.proc = None

        threading.Thread(target=self.connect_to_challenge, daemon=True).start()

    def connect_to_challenge(self):
        try:
            self.ssh = ssh(
                host=CONFIG["host"],
                user=CONFIG["user"],
                password=CONFIG["password"],
                port=CONFIG["port"]
            )
            self.proc = self.ssh.process(CONFIG["binary"], env={"PATH": "/bin:/usr/bin"})
            self.text.insert(END, f"Connected to {CONFIG['challenge_name']}!\n")

            while True:
                output = self.proc.recv(timeout=0.1)
                if output:
                    self.text.insert(END, output.decode(errors='ignore'))
                    self.text.see(END)
        except Exception as e:
            self.text.insert(END, f"Connection error: {e}\n")

    def send_input(self, event):
        cmd = self.entry.get()
        self.entry.delete(0, END)
        if self.proc:
            self.proc.sendline(cmd.encode())


# Start GUI
if __name__ == "__main__":
    root = Tk()
    app = PwnGUI(root)
    root.mainloop()
