# 🤖 Google AI Mode Direct Scraper

A powerful Python-based web scraper that directly interacts with Google's AI Mode to get intelligent answers to your questions. Perfect for educational purposes, research, and learning!

**New:** Now featuring a modular architecture, direct `pip` installation, and native **Android (Termux)** support!

## ✨ Features

- 📝 **Clean Paragraph Answers** - Get AI responses formatted as single, readable paragraphs
- 📊 **Beautiful Table Rendering** - Automatically extracts and displays tables in ASCII format
- 📱 **Mobile Support** - Native support for Termux on Android
- 🎭 **Headless Mode Support** - Run completely in the background or watch it work in real-time
- 🔄 **Batch Processing** - Ask multiple questions in one session
- 💾 **Save Results** - Export all your Q&A sessions to JSON files
- 🛡️ **Anti-Detection** - Enhanced stealth techniques to work reliably

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Google Chrome** installed on your system

### Installation

You can install the tool directly using `pip`.

#### Option 1: Direct Install (Recommended)
Install directly from GitHub without cloning manually. This automatically handles dependencies.

```bash
pip install git+https://github.com/Adwaith673/-Google-AI-Mode-Direct-Scraper.git
```

#### Option 2: Install from Source
If you want to modify the code or run the legacy script:

1. Clone the repository:
   ```bash
   git clone https://github.com/Adwaith673/-Google-AI-Mode-Direct-Scraper.git
   cd -Google-AI-Mode-Direct-Scraper
   ```
2. Install in editable mode:
   ```bash
   pip install -e .
   ```

#### Option 3: Legacy Run
If you don't want to install the package, you can still run the wrapper script after cloning:

```bash
python run_scraper.py
```

## 📱 Running on Android (Termux)

This tool now auto-detects Termux environments!

1. Install system dependencies:
   ```bash
   pkg update
   pkg install python chromium chromedriver
   ```
2. Install the scraper:
   ```bash
   pip install .
   ```
3. Run it:
   ```bash
   google-ai
   ```

## 🎮 Usage

### Headless Mode Selection

When you start the script (`google-ai` or `python run_scraper.py`), you'll see:

```
Configuration:
Run in headless mode? (y/n) [default: n]:
```

- **Type `y`**: Runs completely in the background - super smooth! ⚡
- **Type `n`**: Opens a Chrome window - you'll see it working live. 🪟

### Interactive Commands

Once started, you can use these commands:

#### 1️⃣ Ask Single Questions
```
❓ Ask AI: explain difference btw quantum and normal computer
```

#### 2️⃣ Batch Mode
```
❓ Ask AI: batch

📋 Batch Mode - Enter questions (empty line to finish):
  Question 1: what is machine learning
  Question 2: explain neural networks
  Question 3: [press Enter to finish]
```

#### 3️⃣ Save Results
```
❓ Ask AI: save
Filename [ai_responses.json]: my_research.json
```

#### 4️⃣ Exit
```
❓ Ask AI: quit
```

## 🏗️ Project Structure

The project has been refactored for better maintenance:

```text
.
├── src/google_ai_scraper/
│   ├── core/           # Browser & Parsing Logic
│   ├── utils/          # UI & File Storage
│   └── main.py         # Entry point
├── run_scraper.py      # Legacy wrapper script
└── pyproject.toml      # Packaging configuration
```

## 📋 Example Output

### Response
```
🤖 AI Response (paragraph):
------------------------------------------------------------
The primary difference between a quantum computer and a normal (classical) computer lies in the fundamental principles they use to process information...
------------------------------------------------------------

📊 Table 1:
+-----------------------+--------------------------------------+----------------------------------------------------------------+
| Feature               | Classical Computing                  | Quantum Computing                                              |
+=======================+======================================+================================================================+
| Basic Unit            | Bit (binary digit)                   | Qubit (quantum bit)                                            |
+-----------------------+--------------------------------------+----------------------------------------------------------------+
| Information States    | Can be only 0 or 1.                  | Can be 0, 1, or both simultaneously.                           |
+-----------------------+--------------------------------------+----------------------------------------------------------------+
```

## 🔧 Troubleshooting

### Script won't find AI input box
- ✅ Check `ai_mode_page.html` (debug file) to see what the bot saw.
- ✅ **Mobile/Termux:** Ensure your internet connection is stable; Google might serve a different mobile layout.
- ✅ Try running in non-headless mode (`n`) to debug visually.

### Headless mode fails
- ✅ The script includes auto-detection for system drivers (especially on Termux).
- ✅ If on PC, try updating Chrome and `pip install --upgrade webdriver-manager`.

## ⚠️ Important Notes

### Educational Use Disclaimer
This tool is provided for **educational and research purposes only**. Users should:
- Respect Google's Terms of Service
- Use the tool responsibly and ethically
- Verify all information obtained
- Not use for any commercial scraping at scale

## 🤝 Contributing

Feel free to:
- Report bugs and issues
- Suggest improvements
- Submit pull requests

## 📜 License

This project is for educational purposes. Use responsibly and ethically.

---

**Made with ❤️ for students, researchers, and lifelong learners**