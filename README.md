# 🦉 CLI-Chat

A minimalist, real-time chat client that lives in your terminal — because not everything needs to be a web app.

Built in Python. Runs over WebSockets. Talks like a wise owl.

---

## 🚀 What is This?

CLI-Chat is a lightweight command-line chat app that connects you to a shared chatroom using nothing but your terminal.  
It works on Mac, Linux, and Windows (I even built a `.exe`).

---

## 📦 How to Install

### 🔧 Option 1 — Python Way (for devs)

```bash
git clone https://github.com/Onaga08/CLI-Chat.git
cd CLI-Chat
pip install -r requirements.txt
python chat.py
````

### 🪟 Option 2 — Windows `.exe`  (The Smoothest Way)

1. Go to [Releases](https://github.com/Onaga08/CLI-Chat/releases)
2. Download `chat.exe`
3. Double click
4. Enter nickname + token
5. You’re in 🧙

### 🪟 Option 3 — Mac `Homebrew` (The Smoothest Way)

If you're on macOS and you trust the owl, Homebrew has your back.
Just open Terminal and run:

```bash
brew tap Onaga08/chat
brew install chat
```

Then start chatting with:

```bash
chat
```

### Note - You’ll be prompted to enter your nickname and token — every time. Because owls don’t remember. They just watch. 🦉

---

## 💬 Available Commands

| Command            | Description                    |
| ------------------ | ------------------------------ |
| `list`             | See who's online               |
| `send <user> "hi"` | Send a private message         |
| `global "hi all"`  | Send a message to everyone     |
| `whoami`           | Print your current nickname    |
| `ping`             | Ping the server (just because) |
| `clear`            | Clear the terminal screen      |
| `leave`            | Disconnect                     |
| `help`             | Show command list again        |

---

## 🧠 Why?

Because sometimes, a quiet terminal is all you need.
No bloat. No distractions. Just you and some text-based wisdom.

---

## 🦉 Author

Made by [Onaga08](https://github.com/Onaga08), a night owl.
