# Computer-Stats 👋

Python + Tkinter desktop UI that displays live computer stats (CPU/RAM and related system info) in a clean, compact overlay.
Built as a practical lightweight stats HUD using `psutil`.

<img src="https://github.com/user-attachments/assets/fabd2970-7a07-48ff-aa37-9a5953fb7f4a" alt="Computer-Stats UI screenshot" align="right" width="330" />

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![UI](https://img.shields.io/badge/UI-Tkinter-2ea44f?style=flat-square)](#)
[![Stats](https://img.shields.io/badge/Stats-psutil-4B8BBE?style=flat-square)](https://pypi.org/project/psutil/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)](#)

---

## About This Project
<hr />

- 🖥️ Shows live system stats in a small always-on-top style window.
- ⚡ Updates quickly without heavy dependencies.
- 🧩 One script launches both the clock/date window and the CPU/RAM stats window.

## Files
<hr />

- `ComputerStats.py` — main (combined) script
- `dependencies.txt` — pip dependencies list

## Run
<hr />

Install dependencies:
- `pip install -r dependencies.txt`

Notes:
- `psutil` is required for CPU/RAM stats.
- `keyboard` is optional, but enables arrow-key controls even when the windows are not focused.

Run:
- `python ComputerStats.py`

## Contact
<hr />

- YouTube: https://www.youtube.com/@ModSpidr
- Portfolio: https://gregorybridges.dev
- Email: contact@gregorybridges.dev
