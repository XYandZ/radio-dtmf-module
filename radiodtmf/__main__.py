import argparse
import logging
from radiodtmf.ProgramController import ProgramController

VERSION = "0.2.0"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Listen for DTMF commands and respond with information via text to speech.
        
        Environmental Variables:
        
        | Variable           | Service | Description                             | Default      |
        |--------------------|---------|-----------------------------------------|--------------|
        | ALSA_DEVICE        | Audio   | ALSA Device for audio input and output. | 0            |
        | BME280_IC2_PORT    | BME280  | BME280 IC2 Port.                        | 1            |
        | BME280_IC2_ADDRESS | BME280  | BME280 IC2 Address.                     | 0x76         |
        | SDS011_DEV         | SDS011  | SDS011 dev file                         | /dev/ttyUSB0 |
        """
    )

    parser.add_argument(
        "--version",
        help="Print the program version number and exit.",
        action="version",
        version=f'Radio DTMF Version: {VERSION}'
    )

    parser.add_argument(
        "-d", "--debug",
        help="Print debug information.",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )

    parser.add_argument(
        "-v", "--verbose",
        help="Verbose output.",
        action="store_const", dest="loglevel", const=logging.INFO,
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    pc = ProgramController()
    pc.start()
