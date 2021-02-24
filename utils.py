import re


name_re = re.compile(r"(.+)(_\d+)")
ev_re = re.compile(r"^ev_(\d+)")

def clean_names(text):
    word = ''.join([i if ord(i) < 128 else ' ' for i in text])
    cleaned = re.sub(r'[?|\"|!|\'|#]', r'', word)
    cleaned = re.sub(r'[.|,|;|:|)|(|\|/]', r' ', cleaned)
    cleaned = re.sub(r' ', r'_', cleaned)
    cleaned = cleaned.lower()
    return cleaned

def parse_span_str(span_str):
    _, s, _, w = span_str.split(".")
    return (int(s), int(w))
