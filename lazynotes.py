
# LazyNotesAI v5.0
# AI-Powered Study Revision Assistant
# Model: google/flan-t5-small
# Python 3.9+
#
# Google Colab setup (run in a separate cell):
# !pip -q install transformers sentencepiece torch

import re
from collections import Counter
from pathlib import Path

MODEL_NAME = "google/flan-t5-small"

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "be", "been", "being", "and", "or", "of",
    "to", "in", "on", "at", "for", "by", "with",
    "that", "this", "it", "its", "as", "from",
    "their", "they", "which", "into", "during",
    "has", "have", "had", "also", "called",
    "than", "then", "can", "will", "but",
    "when", "through", "between", "about",
    "there", "each", "every", "such", "other"
}

_tokenizer = None
_model = None


# 1. Load the open-weight AI model
def load_ai_model():
    global _tokenizer, _model

    if _model is not None:
        return

    try:
        from transformers import (
            AutoTokenizer,
            AutoModelForSeq2SeqLM
        )
    except ImportError as error:
        raise RuntimeError(
            "Missing AI packages. In Google Colab, run:\n"
            "!pip install transformers sentencepiece torch"
        ) from error

    print("\nLoading AI model. Please wait...")

    _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    _model.eval()

    print("AI model loaded successfully!")


# 2. Generate text with real AI
def ai_generate(instruction, text, max_tokens=64):
    load_ai_model()

    prompt = f"{instruction}\n\nText: {text}"

    inputs = _tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=480
    )

    outputs = _model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        num_beams=3,
        do_sample=False,
        repetition_penalty=1.3,
        no_repeat_ngram_size=3
    )

    result = _tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return result.strip()


# 3. Split notes into sentences
def split_sentences(notes):
    text = re.sub(r"\s+", " ", notes.strip())

    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if sentence.strip()
    ]


# 4. Extract keywords
def extract_keywords(notes):
    words = re.findall(r"[A-Za-z]+", notes.lower())

    useful = [
        word for word in words
        if len(word) > 3 and word not in STOP_WORDS
    ]

    counts = Counter(useful)

    return [
        word.title()
        for word, count in counts.most_common(10)
    ]


# 5. Build a reliable extractive summary
def generate_ai_summary(notes):
    sentences = split_sentences(notes)

    unique = []
    seen = set()

    for sentence in sentences:
        key = sentence.lower().strip(" .!?")

        if key not in seen:
            unique.append(sentence)
            seen.add(key)

    if not unique:
        return ""

    if len(unique) <= 4:
        return " ".join(unique)

    # Keyword-based sentence selection.
    counts = Counter(
        word.lower()
        for word in re.findall(r"[A-Za-z]+", notes)
        if word.lower() not in STOP_WORDS
    )

    def score(sentence):
        words = re.findall(
            r"[A-Za-z]+", sentence.lower()
        )
        return sum(counts[word] for word in words)

    ranked = sorted(
        range(len(unique)),
        key=lambda i: score(unique[i]),
        reverse=True
    )

    selected = set(ranked[:4])

    return " ".join(
        sentence
        for i, sentence in enumerate(unique)
        if i in selected
    )


# 6. Rule-based backup question
def make_rule_question(sentence):
    sentence = sentence.strip()

    match = re.match(
        r"(.+?)\s+(is|are)\s+(.+)",
        sentence,
        re.IGNORECASE
    )

    if match:
        subject = match.group(1).strip()
        verb = match.group(2).lower()

        if len(subject.split()) <= 7:
            return f"What {verb} {subject.lower()}?"

    match = re.match(
        r"(.+?)\s+contains?\s+(.+)",
        sentence,
        re.IGNORECASE
    )

    if match:
        return (
            "What does "
            + match.group(1).strip().lower()
            + " contain?"
        )

    return f"Explain this statement: {sentence}"


# 7. Generate an AI question
def generate_ai_question(notes):
    sentences = split_sentences(notes)

    if not sentences:
        return None

    # Use one fact to avoid mixing unrelated ideas.
    source = sentences[0]

    question = ai_generate(
        "Write one short study question answered by "
        "the following sentence. Return only the question.",
        source,
        max_tokens=48
    )

    question = question.strip()

    # Reject obvious poor outputs.
    if (
        not question
        or len(question.split()) > 16
        or question.count("?") > 1
        or "\n" in question
    ):
        question = make_rule_question(source)

    question = question.rstrip(".!?") + "?"

    return question, source


# 8. Remove duplicate questions
def remove_duplicate_questions(questions):
    unique = []
    seen_answers = set()
    seen_questions = set()

    for question, answer in questions:
        answer_key = re.sub(
            r"\s+", " ", answer.lower().strip()
        ).rstrip(".!?")

        question_key = re.sub(
            r"\s+", " ", question.lower().strip()
        ).rstrip(".!?")

        if (
            answer_key in seen_answers
            or question_key in seen_questions
        ):
            continue

        unique.append((question, answer))
        seen_answers.add(answer_key)
        seen_questions.add(question_key)

    return unique


# 9. Create revision material
def create_revision(chapter, notes):
    sentences = split_sentences(notes)

    if not sentences:
        raise ValueError("Please enter valid notes.")

    summary = generate_ai_summary(notes)
    keywords = extract_keywords(notes)

    questions = []

    ai_question = generate_ai_question(notes)

    if ai_question:
        questions.append(ai_question)

    for sentence in sentences:
        question = make_rule_question(sentence)
        questions.append((question, sentence))

    questions = remove_duplicate_questions(questions)

    return {
        "chapter": chapter,
        "notes": notes,
        "summary": summary,
        "keywords": keywords,
        "questions": questions[:5]
    }


# 10. Display revision material
def display_revision(revision):
    print("\n" + "=" * 50)
    print("CHAPTER:", revision["chapter"])
    print("=" * 50)

    print("\nREVISION SUMMARY")
    print(revision["summary"])

    print("\nIMPORTANT KEYWORDS")

    if revision["keywords"]:
        for word in revision["keywords"]:
            print("-", word)
    else:
        print("No keywords found.")

    print("\nREVISION QUESTIONS AND ANSWERS")

    for i, (question, answer) in enumerate(
        revision["questions"], 1
    ):
        print(f"\nQ{i}. {question}")
        print(f"Answer: {answer}")


# 11. Create safe filenames
def safe_filename(title):
    name = re.sub(
        r"[^A-Za-z0-9_-]+", "_", title
    )
    return name.strip("_")[:60] or "Untitled"


# 12. Save revision notes
def save_revision(revision):
    folder = Path("saved_notes")
    folder.mkdir(exist_ok=True)

    base = safe_filename(revision["chapter"])
    filename = folder / f"{base}.txt"

    index = 2

    while filename.exists():
        filename = folder / f"{base}_{index}.txt"
        index += 1

    with filename.open(
        "w", encoding="utf-8"
    ) as file:

        file.write("LAZYNOTESAI v5.0\n")
        file.write("=" * 45 + "\n\n")

        file.write(
            f"CHAPTER: {revision['chapter']}\n\n"
        )

        file.write("REVISION SUMMARY\n")
        file.write(revision["summary"] + "\n\n")

        file.write("IMPORTANT KEYWORDS\n")

        for word in revision["keywords"]:
            file.write(f"- {word}\n")

        file.write(
            "\nREVISION QUESTIONS AND ANSWERS\n"
        )

        for i, (question, answer) in enumerate(
            revision["questions"], 1
        ):
            file.write(
                f"\nQ{i}. {question}\n"
                f"Answer: {answer}\n"
            )

        file.write("\nORIGINAL NOTES\n")
        file.write(revision["notes"] + "\n")

    return filename


# 13. Main application
def main():
    print("=" * 52)
    print("             LAZYNOTESAI v5.0")
    print("         AI-Powered Study Assistant")
    print("=" * 52)

    try:
        load_ai_model()
    except Exception as error:
        print("\nCould not load AI model:")
        print(error)
        return

    chapter = input(
        "\nEnter chapter name: "
    ).strip() or "Untitled"

    print("\nPaste your study notes.")
    print("Type DONE on a separate line to finish.\n")

    lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip().upper() == "DONE":
            break

        lines.append(line)

    notes = " ".join(lines).strip()

    if not notes:
        print("\nNo notes entered.")
        return

    print("\nGenerating revision material...")

    try:
        revision = create_revision(chapter, notes)
    except Exception as error:
        print("\nCould not generate revision:")
        print(error)
        return

    display_revision(revision)

    save = input(
        "\nSave revision material? (yes/no): "
    ).strip().lower()

    if save in ("yes", "y"):
        try:
            filename = save_revision(revision)
            print(
                f"\nSaved successfully: {filename}"
            )
        except OSError as error:
            print("\nCould not save notes:", error)
    else:
        print("\nRevision material was not saved.")

    print("\nLazyNotesAI v5.0 finished!")


# 14. Run the application
if __name__ == "__main__":
    main()
