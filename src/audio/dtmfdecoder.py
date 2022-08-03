from pyaudio import PyAudio
from scipy.signal import find_peaks
from numpy import average, absolute, fft, frombuffer, int16
import logging

from src.audio.config import audio_config


class DTMFDecocder:

    DTMF_TABLE = {
        '1': [1209, 697], '2': [1336, 697], '3': [1477, 697], 'A': [1633, 697],
        '4': [1209, 770], '5': [1336, 770], '6': [1477, 770], 'B': [1633, 770],
        '7': [1209, 852], '8': [1336, 852], '9': [1477, 852], 'C': [1633, 852],
        '*': [1209, 941], '0': [1336, 941], '#': [1477, 941], 'D': [1633, 941],
    }

    def __init__(self):

        self.audio = PyAudio()

        config = audio_config()
        self.fs = config["rate"]
        self.chunk = config["frames_per_buffer"]
        self.stream = self.audio.open(**config)

    def __dtmf_decode(self, data, rate):

        # Remove DC component of data
        filtered = data - average(data)

        # Computer unnormalized powr spectral density estimate
        ps = absolute(fft.fft(filtered, rate)**2)

        # Find peaks above the arbitrary threshold of 20 times the average power per frequency
        peaks, _ = find_peaks(ps, 20*average(ps))

        return next( (char for char, frequency_pair in self.DTMF_TABLE.items() if (frequency_pair[0] in peaks) and (frequency_pair[1] in peaks)), None)


    def dtmf_code(self):
        ## start Recording

        last = None
        while True:
            frame = frombuffer(self.stream.read(self.chunk, exception_on_overflow = False), dtype=int16)
            current = self.__dtmf_decode(frame, self.fs)

            logging.debug(current, last)

            if last != current:
                last = current
                if current is not None:
                    yield current
