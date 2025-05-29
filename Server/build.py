import PyInstaller.__main__
import os

# Konfiguriere PyInstaller
PyInstaller.__main__.run([
    'rat_server_gui.py',  # Hauptskript
    '--name=RAT_Server',  # Name der EXE
    '--onefile',  # Einzelne EXE-Datei
    '--windowed',  # Keine Konsole im Hintergrund
    '--icon=NONE',  # Kein Icon (kann später hinzugefügt werden)
    '--clean',  # Lösche temporäre Dateien
    '--noconfirm',  # Keine Bestätigungen
    '--add-data=README.md;.',  # Füge README hinzu
]) 