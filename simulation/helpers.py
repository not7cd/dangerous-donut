import re

_nonbmp = re.compile(r"[\U00010000-\U0010FFFF]")


def _surrogatepair(match):
    char = match.group()
    assert ord(char) > 0xffff
    encoded = char.encode("utf-16-le")
    return chr(int.from_bytes(encoded[:2], "little")) + chr(
        int.from_bytes(encoded[2:], "little")
    )


def with_surrogates(text):
    return _nonbmp.sub(_surrogatepair, text)


def color_from_string(string):
    r = hash(string + "r")
    g = hash(string + "g")
    b = hash(string + "b")

    return "#%02x%02x%02x" % (r % 200 + 50, g % 200 + 50, b % 200 + 50)
