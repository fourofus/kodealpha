# TODO: consider using pkg_resources for managing these strings
# https://stackoverflow.com/questions/1395593/managing-resources-in-a-python-project

GENERAL_RESPONSES = {
    'REPLY_TO_GREETING': 'You are a polite and pleasant person!',
    'REPLY_TO_INSULTING': 'That sounds rude! Are you having a rough day?',
    'GENERAL_REPLY': 'Hello, I am KODE (alpha). Hope you are having a fine day!'
}

ACCEPTED_GREETINGS = [
    "hi",
    "hi there",
    "hello",
    "hey man",
    "how's it going",
    "what's your name?",
    "how are you",
    "how are things",
    "how's everything",
    "how things' going"
    "how's your day",
    "good to see you",
    "good morning",
    "good afternoon",
    "good evening",
    "how have you been",
    "how do you do",
    "yo",
    "are you okay",
    "howdy",
    "sub",
    "hiya",
    "whazzup"
]

KNOWN_INSULTING = [
    "fuck you",
    "dick head",
    "suck it up",
    "what the fuck"
    "die",
    "kill you",
    "shut the fuck up",
    "shut up",
    "moron",
    "asshole",
    "hate you",
    "curse you",
]

INSULTING_KEYWORDS = ['fuck', 'curse', 'dick', 'moron', 'asshole']
