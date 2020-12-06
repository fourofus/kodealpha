from kodealpha.parser import RequestParser


def test_greeting():
    greetings = [
        "hi",
        "Hi there",
        "hello",
        "how ARE you?",
        "how thing's going?",
        "good morning",
        "good to talk to you",
        "good to see you",
        "good afternoon",
        "good evening",
        "hey",
        "hiya",
        "what's your name?",
    ]

    parser = RequestParser()
    for greeting in greetings:
        message_type = parser.parse(greeting)['type']
        assert message_type == RequestParser.MessageType.Greeting, f'"{greeting}" is a greeting.'


def test_non_greeting():
    non_greetings = [
        "what",
        "tell me what?",
        "don't care",
        "shut up",
        "asshole",
        "fuck",
        "what's the weather?",
        "what time is it"
    ]
    parser = RequestParser()
    for non_greeting in non_greetings:
        message_type = parser.parse(non_greeting)['type']
        assert message_type != RequestParser.MessageType.Greeting, f'"{non_greeting}" is not greeting'
