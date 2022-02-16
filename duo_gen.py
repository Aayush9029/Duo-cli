#!/usr/bin/env python3

import logging
from json import JSONDecodeError, dump, load

from pyotp import HOTP

DEBUG = True


class DUO_CLI:
    def __init__(self) -> None:
        self.token_file = "duo_token.json"
        self.secret = None
        self.offset = None

        self.read_token_file()

    def read_token_file(self):
        logging.info(f"Reading token file: {self.token_file}")
        try:
            with open("duo_token.json", "r") as f:
                data = load(f)
                self.secret = data["secret"]
                self.offset = data["offset"]
        except FileNotFoundError:
            logging.error(f"Token file not found: {self.token_file}")
            exit(1)
        except JSONDecodeError:
            logging.error(
                f"Token file is not a valid json file: {self.token_file}")
            exit(1)

    def increment_offset(self):
        logging.info(f"Incrementing current offset: {self.offset} by 1")

        with open("duo_token.json", "w") as f:
            data = {
                "secret": self.secret,
                "offset": self.offset + 1
            }
            dump(data, f, indent=4)
        logging.info("Updating the json file")

    def get_otp(self):
        self.increment_offset()
        return HOTP(self.secret).at(self.offset)


if __name__ == "__main__":
    duo = DUO_CLI()
    print(duo.get_otp())