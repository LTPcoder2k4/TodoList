def trim(txt):
    while len(txt) > 0:
        if txt[0] == ' ':
            txt = txt[1::]
        else:
            break
    while len(txt) > 0:
        if txt[-1] == ' ':
            txt = txt[:-1]
        else:
            break
    i = 0
    while i+1 < len(txt):
        if txt[i] == txt[i+1] == ' ':
            txt = txt[:i] + txt[i+1:]
        else:
            i += 1
    return txt
