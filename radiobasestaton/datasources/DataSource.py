from abc import ABC, abstractmethod


class DataSource(ABC):

    @abstractmethod
    def __init__(self, assigned_code):
        pass

    @abstractmethod
    def assigned_code(self):
        pass

    @staticmethod
    @abstractmethod
    def source_type():
        pass

    @abstractmethod
    def get_data(self):
        pass

    def get_nine_key_code(self, alpha_string):

        def letter_to_nine_key(letter):
            if letter in ['.', ',', '?', '!', ':']:
                return 1
            elif letter in ['A', 'B', 'C']:
                return 2
            elif letter in ['D', 'E', 'F']:
                return 3
            elif letter in ['G', 'H', 'I']:
                return 4
            elif letter in ['J', 'K', 'L']:
                return 5
            elif letter in ['M', 'N', 'O']:
                return 6
            elif letter in ['P', 'Q', 'R', 'S']:
                return 7
            elif letter in ['T', 'U', 'V']:
                return 8
            elif letter in ['W', 'X', 'Y', 'Z']:
                return 9

        [letter_to_nine_key(letter) for letter in alpha_string]
