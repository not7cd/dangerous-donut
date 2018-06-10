import re

_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')

def _surrogatepair(match):
    char = match.group()
    assert ord(char) > 0xffff
    encoded = char.encode('utf-16-le')
    return (
        chr(int.from_bytes(encoded[:2], 'little')) + 
        chr(int.from_bytes(encoded[2:], 'little')))

def with_surrogates(text):
    return _nonbmp.sub(_surrogatepair, text)

def color_from_string(string):
    r = hash(string)
    g = hash(string[1:])
    b = hash(string[2:])

    return '#%02x%02x%02x' % (r%255, g%255, b%255)