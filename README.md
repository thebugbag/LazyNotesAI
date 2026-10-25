
# 📚 LazyNotesAI v5.0

**Turn your study notes into useful revision material with Python and open-weight AI!**

LazyNotesAI is an open-source, command-line study assistant that helps students revise their lessons.

Version 5.0 integrates Google's **FLAN-T5-small** language model through Hugging Face Transformers to generate study questions. It combines AI with reliable rule-based processing for summaries, keywords, and revision answers.

## ✨ Features

- 🤖 Generates an AI-assisted study question using FLAN-T5-small
- 📝 Creates extractive summaries from original notes
- 🔑 Extracts important keywords
- ❓ Generates revision questions and answers
- 🔁 Removes questions with identical answers
- 💾 Saves revision material as `.txt` files
- 📂 Prevents overwriting previously saved files
- ☁️ Runs in Google Colab without installing Python packages on your computer

## 🧠 How the AI Works

LazyNotesAI uses the open-weight model:

**`google/flan-t5-small`**

The model reads a factual sentence from the student's notes and generates a revision question.

Other features use Python-based processing:

| Feature | Technology |
|---|---|
| Study question generation | FLAN-T5-small AI model |
| Summary generation | Extractive sentence selection |
| Keyword extraction | Python word-frequency analysis |
| Additional questions | Rule-based question templates |
| Duplicate removal | Answer and question matching |
| Saving revision notes | Python file handling |

This hybrid approach keeps answers grounded in the student's original notes.

## 🚀 Getting Started — Google Colab

Google Colab is recommended for beginners.

### Step 1: Open Google Colab

Visit https://colab.research.google.com/

Create a new Python notebook.

### Step 2: Install Dependencies

Run this in a code cell:

```python
!pip -q install transformers sentencepiece torch
```

### Step 3: Download LazyNotesAI

Run this in a new code cell:

```python
!wget -q -O lazynotes.py https://raw.githubusercontent.com/thebugbag/LazyNotesAI/main/lazynotes.py
```

### Step 4: Run the App

Run:

```python
!python lazynotes.py
```

Enter a chapter name, paste your notes, and type `DONE` on a separate line.

**Note:** The app is interactive. If the Colab `!python` cell does not accept input correctly, use the following alternative in a Python cell:

```python
import lazynotes
lazynotes.main()
```

## 📖 Example

**Chapter:** Atomic Structure

**Input notes:**

```text
An atom is the smallest unit of an element.
The nucleus contains protons and neutrons.
Electrons have a negative charge.
The atomic number equals the number of protons.
```

**Example revision questions:**

```text
Q1. What is the smallest unit of an element?
Answer: An atom is the smallest unit of an element.

Q2. What does the nucleus contain?
Answer: The nucleus contains protons and neutrons.
```

The exact AI-generated question may vary with model and library versions.

## 💾 Saving Notes

When prompted, type `yes` to save the revision material.

The program creates a folder named:

```text
saved_notes/
```

Files are saved using the chapter name, for example:

```text
saved_notes/Atomic_Structure.txt
```

If a filename already exists, a numbered filename is created instead.

**Google Colab reminder:** Files saved in the Colab runtime may disappear when the session ends. Download important files before closing the runtime.

## ⚙️ Requirements

- Python 3.9 or newer
- `transformers`
- `sentencepiece`
- `torch`
- Internet connection for the first model download
- Sufficient memory to load FLAN-T5-small

## ⚠️ Current Limitations

- Best suited for short, factual English notes
- AI question quality may vary
- The summary is extractive, not a generative AI summary
- Some questions use simple rule-based templates
- Duplicate filtering may not catch all similar questions
- The model's input is truncated when notes exceed the supported length
- AI-generated questions should be reviewed for accuracy

## 🛠️ Built With

- Python
- Hugging Face Transformers
- Google FLAN-T5-small
- PyTorch
- Google Colab

## 🌱 Project Journey

LazyNotesAI began as a lightweight rule-based revision tool in version 4.2.

Version 5.0 introduces an open-weight language model for question generation while keeping the original note-processing features.

Future improvements may include more flexible question generation, stronger summaries, and better support for longer notes.

## 🤝 Contributing

Suggestions, bug reports, documentation improvements, and pull requests are welcome.

Please open an issue to discuss major changes before submitting them.

## 📄 License

See the [LICENSE](LICENSE) file for this project's license.

---

**LazyNotesAI — Study smarter, one chapter at a time.** 📚
