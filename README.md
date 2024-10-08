# PyJi

**PyJi** is a flexible flashcard application to help you learn and memorize any subject. It is floating desktop app above all other windows, displaying random questions from a deck. The main purpose of the application is to continuously show questions, kanji, or any content, so that the user passively memorizes them.
<p align="center">
  <img src="https://github.com/user-attachments/assets/52b38abc-e6b0-4814-aed2-cf350f984f47" alt="PyJi Example 1">
  <img src="https://github.com/user-attachments/assets/04e34489-127a-4141-9627-a93cbce1e968" alt="PyJi Example 2">
</p>

## Features

- **Cross-Platform**: Runs on Windows, macOS, and Linux.
- **Flexible Deck Management**: Load and organize decks on any subject.

## Made using

- **Python** 3.6+
- **Qt** via [PySide6](https://pypi.org/project/PySide6/) for the GUI
- **PyYAML** for deck file handling

## Deck Format

Deck files should be in YAML format:

```yaml
decks:
  - name: 'Deck Name'
    cards:
      - ['Question', 'Answer', 'Optional Comment']
      - ['口', 'こう・くち', 'Mouth']
      - ['目', 'もく・め', 'Eye']
```

## Deck Placement

Place your `.yaml` deck files in the `decks` directory within the application's config folder:

- **Windows**: `C:\Users\<YourUserName>\AppData\Roaming\PyJi\decks`
- **macOS**: `/Users/<YourUserName>/Library/Application Support/PyJi/decks`
- **Linux**: `/home/<YourUserName>/.config/PyJi/decks`

---

Start using PyJi for efficient and flexible learning!
