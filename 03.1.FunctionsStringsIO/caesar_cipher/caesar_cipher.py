def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    out_str_list = []
    for sym in message:
        if not sym.isalpha():
            out_str_list.append(sym)
            continue
        else:
            if sym.islower():
                start = ord('a')
            else:
                start = ord('A')
            out_str_list.append(chr(start + (ord(sym) - start + n) % 26))
    return ''.join(out_str_list)
