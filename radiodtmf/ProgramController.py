from operator import add
from functools import reduce
from time import sleep
from pyttsx3 import speak

from radiodtmf.audio import DTMFDecocder
from radiodtmf.datasources import *
from radiodtmf.datasources.config import config
from radiodtmf.datasources.SourceTypes import SourceType


class ProgramController():

    def __init__(self):

        cfg = config("services")

        def get_nine_key_code(alpha_string):

            def letter_to_nine_key(letter):
                if letter in ['.', ',', '?', '!', ':']:
                    return '1'
                elif letter in ['A', 'B', 'C']:
                    return '2'
                elif letter in ['D', 'E', 'F']:
                    return '3'
                elif letter in ['G', 'H', 'I']:
                    return '4'
                elif letter in ['J', 'K', 'L']:
                    return '5'
                elif letter in ['M', 'N', 'O']:
                    return '6'
                elif letter in ['P', 'Q', 'R', 'S']:
                    return '7'
                elif letter in ['T', 'U', 'V']:
                    return '8'
                elif letter in ['W', 'X', 'Y', 'Z']:
                    return '9'

            return reduce(add, map(letter_to_nine_key,  alpha_string))

        self.modules = {}

        for module, code in {module:code for module, code in cfg.items() if module in [x.name for x in SourceType]}.items():
            nine_key_code = get_nine_key_code(code)
            self.modules[nine_key_code] = next( cls(nine_key_code) for cls in DataSource.__subclasses__() if cls.source_type() == SourceType[module] )

        self.dtmf_decoder = DTMFDecocder()

    def __build_help_menu(self):
        return "Available Commands. " + ", ".join([str(cls) for cls in self.modules.values()])

    def __get_info_from_dtmf_code(self, code):
        if code in self.modules.keys():
            return self.modules[code].get_data()
        else:
            return None

    def start(self):

        # reduce( lambda x,y : x + y, self.dtmf_decoder.dtmf_code(), '')
        def speak_with_delay(phrase):
            sleep(2)
            speak(phrase)

        seq = ""

        for x in self.dtmf_decoder.dtmf_code():

            if x == "#":
                speak_with_delay(self.__build_help_menu())
                seq = ""
            else:
                seq = seq + x

            if seq in self.modules.keys():
                speak_with_delay(self.__get_info_from_dtmf_code(seq))
                seq = ""
                continue

            if len(seq) > max([len(x) for x in self.modules.keys()]):
                seq = x