# 📚 LazyNotesAI

**Turn your study notes into revision material using Python!**

LazyNotesAI is a lightweight, rule-based study revision assistant built with Python. It helps students organize their notes into summaries, important keywords, and practice questions with answers.

## ✨ Features

- 📝 Generates quick summaries from study notes
- 🔑 Extracts important keywords
- ❓ Creates revision questions and answers
- 💾 Saves revision material as text files
- 📂 Automatically avoids overwriting existing saved notes
- ⚡ Runs without external Python packages
- 🖥️ Works through a simple command-line interface

## 🚀 Getting Started

**Requirements:** Python 3.9 or newer.

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python3 lazynotes.py
```

4. Enter your chapter name.
5. Paste your notes.
6. Type `DONE` on a separate line and press Enter.
7. Review the generated revision material.
8. Type `yes` when prompted to save it.

## 📖 Example

**Input:**

An atom is the smallest unit of an element that retains its chemical properties.

**Generated question:**

Q: What is an atom?

A: An atom is the smallest unit of an element that retains its chemical properties.

## 🛠️ How It Works

LazyNotesAI uses Python's built-in libraries, regular expressions, keyword frequency analysis, and predefined question-generation rules.

It does not use a large language model or external AI service. Results depend on the structure and quality of the input notes.

## 🔮 Future Improvements

- Better question generation
- More balanced summaries
- Multiple-choice quizzes
- Interactive revision mode
- Improved handling of different subjects

## 📜 License

This project is available under the MIT License. See the `LICENSE` file for details.

---

**Built for students who want to revise smarter.**
