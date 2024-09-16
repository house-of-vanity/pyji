# PyJi

**PyJi** is a simple and convenient application for learning Japanese kanji using flashcards. The program allows you to manage card decks, display random kanji, their readings, and translations, helping you effectively memorize new symbols.

## Features

- **Deck Management**: Load and select decks for study.
- **Interface Customization**: Change the card update interval, window transparency, background and text colors.
- **Interactive Learning**: Display new cards at specified time intervals, with the ability to pause and resume the timer.
- **Information Display**: Large font for kanji and smaller font for readings and translations, convenient switching between sides of the card.

## Installation

### Requirements

- **Python** 3.6 or higher
- **Python Libraries**:
  - [PySide6](https://pypi.org/project/PySide6/)
  - [PyYAML](https://pypi.org/project/PyYAML/)

### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/pyji.git
   ```

2. **Navigate to the project directory**

   ```bash
   cd pyji
   ```

3. **Create and activate a virtual environment (recommended)**

   - On Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   If the `requirements.txt` file is missing, install the necessary libraries manually:

   ```bash
   pip install PySide6 PyYAML
   ```

## Usage

1. **Run the application**

   ```bash
   python main.py
   ```

2. **Add decks**

   - Create a `decks` directory in the application's configuration folder:

     - **Windows**: `C:\Users\<YourUserName>\AppData\Roaming\PyJi\decks`
     - **Linux/macOS**: `/home/<YourUserName>/.config/PyJi/decks`

   - Place deck files in YAML format into this directory. Sample decks are available in the repository in the `decks` folder.

3. **Manage decks**

   - Run the application.
   - Click on the settings icon (gear).
   - In the settings, select **Deck Manager**.
   - Check the decks you want to use and save changes.

4. **Study cards**

   - The application will automatically display random kanji from the selected decks.
   - **Left-click** on the card:
     - Pause or resume the timer.
     - When resuming the timer, the next card is shown immediately.
   - **Right-click** on the card:
     - Displays the readings and translation of the kanji.
     - The timer is paused for convenient study.
     - A subsequent right-click returns to the kanji.

## Settings

- **Update Interval**: Sets the time (in seconds) between card changes.
- **Window Transparency**: Adjusts the transparency level of the main window.
- **Background and Text Color**: Allows you to customize the appearance of the application to your preferences.
- **Pin Window**: Ability to keep the window on top of others for constant access.

## Deck Format

Deck files must be in YAML format with the following structure:

```yaml
decks:
  - name: 'Deck Name'
    cards:
      - ['Kanji', 'Readings', 'Translation']
      - ['一', 'いち・ひとつ', 'One']
      # Add more cards here
```

## Sample Decks

- **N5 Kanji Deck**: Includes 50 popular N5-level kanji.
- **N4 Kanji Deck**: Includes 50 popular N4-level kanji.

## Contributing

We welcome your contributions to the development of **PyJi**! You can:

- **Report bugs**: Open a new [Issue](https://github.com/yourusername/pyji/issues) on GitHub.
- **Suggest enhancements**: Share your ideas through Issues or Pull Requests.
- **Add new decks**: Create your own decks and share them with the community.

## License

This project is distributed under the [MIT License](LICENSE).

## Contact

- **Author**: [Your Name or Nickname]
- **Email**: your.email@example.com

## Acknowledgments

Thank you to everyone who supports and uses **PyJi**! Your feedback and suggestions help make the application better.

---

**Note**: Replace `https://github.com/yourusername/pyji` with the actual URL of your GitHub repository. Also, update the contact information and add a `LICENSE` file if necessary.