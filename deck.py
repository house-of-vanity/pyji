import random
import yaml
import os


def read_yaml(file_path):
    """
    Read YAML data from a file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data


def is_valid_deck_data(data):
    """
    Check if the provided data is a valid deck structure.
    """
    # Valid if it has a 'decks' key with a list of decks
    return isinstance(data, dict) and 'decks' in data and isinstance(data['decks'], list)


def load_all_decks(directory_path):
    """
    Load all valid decks from YAML files in the specified directory into a dictionary.
    """
    all_decks = {}

    # Iterate through all files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.yaml'):  # Process only YAML files
            file_path = os.path.join(directory_path, file_name)
            try:
                data = read_yaml(file_path)
                if is_valid_deck_data(data):
                    for deck in data['decks']:
                        deck_name = deck['name']
                        if deck_name not in all_decks:
                            all_decks[deck_name] = []
                        # Append cards to the existing deck
                        all_decks[deck_name].extend(deck['cards'])
                else:
                    print(f"Invalid deck format in file: {file_name}")
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    return all_decks


class Collection:
    def __init__(self, directory_path):
        """
        Initialize the Collection by loading all valid decks from YAML files in the given directory.
        """
        self.decks = load_all_decks(directory_path)

    def get_random_card(self, deck_name):
        """
        Get a random card from the specified deck.
        """
        if deck_name not in self.decks:
            raise ValueError(f"Deck '{deck_name}' not found in the collection.")

        cards = self.decks[deck_name]
        if not cards:
            raise ValueError(f"No cards available in the deck '{deck_name}'.")

        return random.choice(cards)

    def get_decks(self):
        """
        Get a list of all available deck names.
        """
        return list(self.decks.keys())
