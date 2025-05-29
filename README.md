

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/your_username/RAT">
    ">
  </a>

  <h3 align="center">RAT (Remote Access Tool)</h3>

  <p align="center">
    Ein einfaches Remote Access Tool (RAT) in Python, das es ermöglicht, Befehle auf einem entfernten System auszuführen und Informationen abzurufen.
    <br />
    <a href="https://github.com/your_username/RAT"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/your_username/RAT">View Demo</a>
    &middot;
    <a href="https://github.com/your_username/RAT/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/your_username/RAT/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#commands">Commands</a></li>
    <li><a href="#categories">Categories</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Ein einfaches Remote Access Tool (RAT) in Python, das es ermöglicht, Befehle auf einem entfernten System auszuführen und Informationen abzurufen.

### Built With

* [Python](https://www.python.org/)
* [Socket](https://docs.python.org/3/library/socket.html)
* [PIL (Pillow)](https://pillow.readthedocs.io/)
* [pyperclip](https://pypi.org/project/pyperclip/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3.6 oder höher
* pip (Python Package Manager)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/your_username/RAT.git
   ```
2. Installiere die benötigten Pakete
   ```sh
   pip install pyperclip pillow
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Server (Listener)

Starte den Listener auf dem Server (z.B. mit ncat):
```sh
ncat -lvnp 8080
```

### Client

Starte den Client auf dem Zielsystem:
```sh
python rat.py
```

Der Client verbindet sich automatisch mit dem Server und wartet auf Befehle.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- COMMANDS -->
## Commands

Das RAT unterstützt eine Vielzahl von Befehlen, die in Kategorien unterteilt sind:

### System-Informationen
- `os` – Betriebssystemname und Version
- `hostname` – Rechnername
- `whoami` – Aktuell angemeldeter Benutzer
- `users` – Alle eingeloggten Benutzer
- `env` – Umgebungsvariablen anzeigen
- `cpu` – CPU-Informationen
- `memory` – RAM-Auslastung
- `disk` – Festplattenplatz
- `uptime` – Systemlaufzeit
- `ipconfig` – Netzwerk-Konfiguration
- `netstat` – Offene Netzwerkverbindungen
- `lsusb` – USB-Geräte (Linux/Mac)
- `lspci` – PCI-Geräte (Linux)

### Dateisystem
- `cwd` – Aktuelles Arbeitsverzeichnis
- `listdir <pfad>` – Dateien/Ordner auflisten
- `tree <pfad>` – Verzeichnisbaum anzeigen
- `mkdir <pfad>` – Verzeichnis erstellen
- `rmdir <pfad>` – Verzeichnis löschen
- `delete <pfad>` – Datei löschen
- `download <pfad>` – Datei als Base64 senden
- `upload <pfad> <base64>` – Datei aus Base64 speichern

### Prozesse & Benutzer
- `processes` – Laufende Prozesse anzeigen
- `kill <pid>` – Prozess beenden
- `start <befehl>` – Prozess starten

### Netzwerk
- `ping <host>` – Host anpingen
- `traceroute <host>` – Route zu Host anzeigen
- `ifconfig` – Netzwerkschnittstellen (Linux/Mac)
- `route` – Routing-Tabelle anzeigen

### Systemsteuerung
- `shutdown` – Rechner herunterfahren
- `reboot` – Rechner neu starten
- `logoff` – Benutzer abmelden
- `lock` – Bildschirm sperren (Windows)

### Clipboard & Screenshot
- `clipboard` – Inhalt der Zwischenablage anzeigen
- `screenshot` – Screenshot als Base64 senden

### Text/Utility
- `echo <text>` – Text zurückgeben
- `reverse <text>` – Text rückwärts ausgeben
- `help` – Hilfe anzeigen

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CATEGORIES -->
## Categories

Die Befehle sind in Kategorien unterteilt, um die Übersichtlichkeit zu erhöhen. Gib `help` ein, um alle verfügbaren Befehle zu sehen.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/your_username/RAT/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Max 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/your_username/RAT.svg?style=for-the-badge
[contributors-url]: https://github.com/your_username/RAT/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/your_username/RAT.svg?style=for-the-badge
[forks-url]: https://github.com/your_username/RAT/network/members
[stars-shield]: https://img.shields.io/github/stars/your_username/RAT.svg?style=for-the-badge
[stars-url]: https://github.com/your_username/RAT/stargazers
[issues-shield]: https://img.shields.io/github/issues/your_username/RAT.svg?style=for-the-badge
[issues-url]: https://github.com/your_username/RAT/issues
[license-shield]: https://img.shields.io/github/license/your_username/RAT.svg?style=for-the-badge
[license-url]: https://github.com/your_username/RAT/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/your_username
[product-screenshot]: images/screenshot.png 
