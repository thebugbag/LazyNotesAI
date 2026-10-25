

import re
from collections import Counter
from pathlib import Path

# ==========================================
# LAZYNOTES VERSION 4.2
# Smart Study Revision Assistant
# Python 3.9+ | No external packages
# ==========================================

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "be", "been", "being", "and", "or", "of",
    "to", "in", "on", "at", "for", "by", "with",
    "that", "this", "it", "its", "as", "from",
    "their", "they", "which", "into", "during",
    "has", "have", "had", "also", "called",
    "than", "then", "can", "will", "but",
    "when", "through", "between", "about",
    "there", "each", "every", "such", "other",
    "states", "state", "found", "equal",
    "different", "total", "present", "number",
    "type", "process", "thing", "things"
}


def split_sentences(notes):
    text = re.sub(r"\s+", " ", notes.strip())

    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if sentence.strip()
    ]


def clean_subject(subject):
    return subject.strip().rstrip(" .?!")


def question_subject(subject):
    subject = clean_subject(subject)
    subject = subject[0].lower() + subject[1:] if subject else subject

    # Preserve a/an/the for natural grammar.
    return subject


def keywords_from_notes(notes):
    words = re.findall(r"[A-Za-z]+", notes.lower())

    useful = [
        word for word in words
        if len(word) > 3 and word not in STOP_WORDS
    ]

    return Counter(useful)


def make_summary(sentences, frequency):
    if len(sentences) <= 5:
        return sentences[:]

    # Choose around 60% for better concept coverage.
    count = max(3, round(len(sentences) * 0.6))

    def score(sentence):
        words = re.findall(r"[A-Za-z]+", sentence.lower())
        useful = [w for w in words if w not in STOP_WORDS]

        keyword_score = (
            sum(frequency[w] for w in useful) / len(useful)
            if useful else 0
        )

        bonus = 0

        if re.search(r"\b(is|are)\b", sentence, re.I):
            bonus += 1.5

        if re.search(r"\blaw\b.*\bstates\b", sentence, re.I):
            bonus += 2

        if re.search(r"\b(formula|equation)\b", sentence, re.I):
            bonus += 2

        if re.search(r"\b(isotopes?|atomic number|mass number)\b",
                     sentence, re.I):
            bonus += 1.5

        return keyword_score + bonus

    ranked = sorted(
        range(len(sentences)),
        key=lambda i: score(sentences[i]),
        reverse=True
    )

    selected = set(ranked[:count])

    return [
        sentence for i, sentence in enumerate(sentences)
        if i in selected
    ]


def make_question(sentence):
    sentence = sentence.strip()

    # Laws: "Newton's second law states that..."
    match = re.match(
        r"(.+?\blaw(?:\s+of\s+\w+)?)\s+states\s+that\b",
        sentence,
        re.I
    )

    if match:
        return f"What does {question_subject(match.group(1))} state?"

    # Formula statements
    match = re.match(
        r"(?:The\s+)?(?:mathematical\s+)?formula\s+for\s+"
        r"(.+?)\s+is\b",
        sentence,
        re.I
    )

    if match:
        return f"What is the formula for {match.group(1).strip()}?"

    # "The nucleus contains..."
    match = re.match(r"(.+?)\s+contains?\s+(.+)", sentence, re.I)

    if match:
        return (
            f"What does {question_subject(match.group(1))} contain?"
        )

    # "Electrons occupy..."
    match = re.match(r"(.+?)\s+occupy\s+(.+)", sentence, re.I)

    if match:
        return (
            f"What do {question_subject(match.group(1))} occupy?"
        )

    # Definitions: "An atom is...", "Isotopes are..."
    match = re.match(
        r"(.+?)\s+(is|are)\s+(.+)",
        sentence,
        re.I
    )

    if match:
        subject = question_subject(match.group(1))
        verb = match.group(2).lower()

        if 1 <= len(subject.split()) <= 7:
            return f"What {verb} {subject}?"

    # Common science verbs
    patterns = [
        (r"(.+?)\s+absorbs?\s+(.+)", "absorb"),
        (r"(.+?)\s+provides?\s+(.+)", "provide"),
        (r"(.+?)\s+opposes?\s+(.+)", "oppose"),
        (r"(.+?)\s+produces?\s+(.+)", "produce"),
        (r"(.+?)\s+releases?\s+(.+)", "release"),
        (r"(.+?)\s+uses?\s+(.+)", "use"),
        (r"(.+?)\s+requires?\s+(.+)", "require"),
    ]

    for pattern, verb in patterns:
        match = re.match(pattern, sentence, re.I)

        if match:
            subject = question_subject(match.group(1))

            if len(subject.split()) <= 7:
                return f"What does {subject} {verb}?"

    # Fallback that always keeps the original context.
    return f"Explain this statement: {sentence}"


def safe_filename(title):
    name = re.sub(r"[^A-Za-z0-9_-]+", "_", title)
    return name.strip("_")[:60] or "Untitled"


def save_notes(chapter, notes, summary, keywords, questions):
    folder = Path("saved_notes")
    folder.mkdir(exist_ok=True)

    base = safe_filename(chapter)
    filename = folder / f"{base}.txt"

    index = 2

    while filename.exists():
        filename = folder / f"{base}_{index}.txt"
        index += 1

    with filename.open("w", encoding="utf-8") as file:
        file.write("LAZYNOTES VERSION 4.2\n")
        file.write("=" * 45 + "\n")
        file.write(f"CHAPTER: {chapter}\n\n")

        file.write("QUICK SUMMARY\n")
        for sentence in summary:
            file.write("- " + sentence + "\n")

        file.write("\nIMPORTANT KEYWORDS\n")
        for word in keywords:
            file.write("- " + word + "\n")

        file.write("\nREVISION QUESTIONS & ANSWERS\n")
        for i, (question, answer) in enumerate(questions, 1):
            file.write(f"\nQ{i}. {question}\n")
            file.write(f"Answer: {answer}\n")

        file.write("\nORIGINAL NOTES\n")
        file.write(notes + "\n")

    return filename


def main():
    print("=" * 50)
    print("       LAZYNOTES — VERSION 4.2")
    print("       Smart Study Revision Assistant")
    print("=" * 50)

    chapter = input("\nEnter chapter name: ").strip()
    if not chapter:
        chapter = "Untitled"

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

    sentences = split_sentences(notes)

    if not sentences:
        print("\nNo valid sentences found.")
        return

    frequency = keywords_from_notes(notes)
    summary = make_summary(sentences, frequency)

    keywords = [
        word.title()
        for word, count in frequency.most_common(10)
    ]

    questions = [
        (make_question(sentence), sentence)
        for sentence in sentences
    ]

    print("\n" + "=" * 50)
    print("CHAPTER:", chapter)
    print("=" * 50)

    print("\n📝 QUICK SUMMARY")
    for sentence in summary:
        print("•", sentence)

    print("\n⭐ IMPORTANT KEYWORDS")
    if keywords:
        for word in keywords:
            print("•", word)
    else:
        print("No keywords found.")

    print("\n❓ REVISION QUESTIONS & ANSWERS")
    for i, (question, answer) in enumerate(questions, 1):
        print(f"\nQ{i}. {question}")
        print(f"Answer: {answer}")

    print("\n" + "=" * 50)

    save = input(
        "Save revision material? (yes/no): "
    ).strip().lower()

    if save in ("yes", "y"):
        try:
            filename = save_notes(
                chapter, notes, summary, keywords, questions
            )
            print(f"\n✅ Saved successfully: {filename}")
        except OSError as error:
            print(f"\n❌ Could not save file: {error}")
    else:
        print("\nRevision material was not saved.")

    print("\n🎉 LazyNotes Version 4.2 finished!")


if __name__ == "__main__":
    main()
