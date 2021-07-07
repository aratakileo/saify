def count(text: str) -> str:
    char = text[:1]
    char_count = 1
    result = ''

    def append():
        nonlocal result
        result += f'{char}{char_count}'

    def final_append(i: int):
        nonlocal result
        if i == len(text[1:]) - 1:
            append()

    for i in range(len(text[1:])):
        _char = text[1:][i]
        if _char == char:
            char_count += 1
            final_append(i)
        else:
            append()
            char = _char
            char_count = 1
            final_append(i)

    return result


def chunk(text: str, __len: int = 1) -> list:
    return [text[0+i:__len+i] for i in range(0, len(text), __len)]


def replace(text: str, __dict: dict) -> str:
    for key in list(__dict.keys()):
        text = text.replace(key, __dict[key])

    return text
