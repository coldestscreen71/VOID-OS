🖥️ VOID-OS

A terminal-based pseudo operating system built in Python, featuring a custom command interpreter, virtual file system, executable scripts, and ASCII-based media rendering.

---

🚀 Overview

VOID-OS is a simulation of an operating system environment inside the terminal.
It allows users to interact with a structured file system, execute custom commands, and even render images and videos as ASCII.

This project focuses on system design concepts like abstraction, command parsing, file handling, and modular architecture.

---

✨ Features

- 🧠 Custom command interpreter
- 📁 Virtual file system (directories, files, metadata)
- ⚙️ Executable ".exe" scripts
- 📝 Built-in text editor
- 🖼️ ASCII image rendering (".img")
- 🎬 ASCII video playback (".vid")
- 📜 Command history (arrow key navigation)
- ❗ Centralized error handling system
- 🎨 Colored terminal output

---

🧪 Example Commands

# File system
mkdir test
cd test
touch hello.txt
write hello.txt Hello World
cat hello.txt

# Executable scripts
touch script.exe
edit script.exe
execute script.exe

# Image rendering
img photo.jpg art
view art.img

# Video rendering
vid video.mp4 movie
play movie.vid

---

🏗️ Project Structure

VOID-OS/
│
├── commands/        # Command implementations
├── media/           # Image & video processing
├── system/          # Filesystem & data handling
├── main.py          # Entry point
└── terminal.py      # Command parser & terminal loop

---

⚙️ How It Works

VOID-OS is built around layered architecture:

User Input → Command Parser → Commands → Filesystem API → Data Layer

- Commands interact with a virtual file system
- Files store metadata + external data separately
- Media is converted into ASCII and stored as text
- Executable files run line-by-line commands

---

🧠 Concepts Used

- Command parsing ("shlex")
- File system simulation
- Data abstraction (metadata vs content)
- Modular architecture
- Error handling systems
- ASCII rendering techniques

---

▶️ Running the Project

python main.py

---

⚠️ Notes

- This is a simulated OS, not a real one
- Some features are experimental (especially video rendering)
- Performance may vary depending on input size

---

🚧 Future Improvements

- Path system ("/home/user/file.txt")
- Command piping ("|", "&&")
- Flags support ("-a", "-f")
- Performance optimization
- UI improvements

---

📌 Author

Gopal Mahato
GitHub: https://github.com/coldestscreen71

---

🗿 Final Note

This project started as a simple idea and evolved into a full system simulation.
It reflects learning, experimentation, and building from scratch.

More improvements coming soon 🚀
