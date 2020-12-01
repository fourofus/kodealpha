from difflib import SequenceMatcher
from enum import Enum, auto

# 17 Useful English Greetings: https://www.fluentu.com/blog/english/english-greetings-expressions/
from kodealpha.strings import ACCEPTED_GREETINGS, INSULTING_KEYWORDS


class RequestParser:
    """
    This itself parses a message but should be able to outsource its job to a third party via HTTP.
    """
    GREETING_THRESHOLD = 0.6
    INSULTING_THRESHOLD = 0.5

    CHAR_LENGTH_TO_COMPARE = 10

    class MessageType(Enum):
        Greeting = auto(),
        Insulting = auto(),
        WeatherQuery = auto(),
        Unknown = auto()

    def guess_message_type(self, message: str) -> MessageType:
        greeting_score = 0.0
        insulting_score = 0.0

        message = message.lower()
        message = message[:self.CHAR_LENGTH_TO_COMPARE]

        for greeting in ACCEPTED_GREETINGS:
            ratio = SequenceMatcher(None, a=greeting, b=message).ratio()
            greeting_score = ratio if ratio > greeting_score else greeting_score

        for insulting_keyword in INSULTING_KEYWORDS:
            if insulting_keyword in message:
                insulting_score = self.INSULTING_THRESHOLD

        if greeting_score >= self.GREETING_THRESHOLD:
            print(f'{message}: {greeting_score}')
            return self.MessageType.Greeting
        if insulting_score >= self.INSULTING_THRESHOLD:
            return self.MessageType.Insulting
        return self.MessageType.Unknown

    def parse(self, message: str) -> dict:
        return {
            '_raw': 'message',
            'type': self.guess_message_type(message),
        }
