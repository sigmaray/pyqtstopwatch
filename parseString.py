"""Module that parses time interval inputted by user (is used in timer.pyw)"""

def doesEndWithQualifier(userInput):
    """
    Determine if time interval inputted by user ends with 's'/'m'/'h'/'d'/'w'
    """
    if not userInput:
        return False
    if len(userInput) == 0:
        return False
    last = userInput[len(userInput) - 1]
    return last in ['s', 'm', 'h', 'd', 'w']

def withoutQualifier(userInput):
    """
    Remove 's'/'m'/'h'/'d'/'w' from the end of value inputted by user
    (leaves only number)
    """
    if len(userInput) == 0:
        return userInput

    stripped = userInput.strip()

    if not stripped:
        return stripped

    if not doesEndWithQualifier(stripped):
        return float(stripped)

    return float(stripped[:-1])

def getQualifierMult(userInput): # pylint: disable=too-many-return-statements
    """
    Determine multiplier for a string inputted by user
    If user input doesn't have 's'/'m'/'h'/'d'/'w' in the end return 1
    If input does have 's'/'m'/'h'/'d'/'w' return int value that corresponds to
    qualifier (1/60/360...)
    """
    if len(userInput) == 0:
        return 1

    stripped = userInput.strip()

    if not stripped:
        return 1

    if not doesEndWithQualifier(stripped):
        return 1

    mult = stripped[-1]

    if mult == 's':
        return 1

    if mult == 'm':
        return 60

    if mult == 'h':
        return 60*60

    if mult == 'd':
        return 60*60*24

    if mult == 'w':
        return 60*60*24*7

    return 1

def isStringValid(userInput):
    """
    Check if user input is valid
    """
    stripped = userInput.strip()

    if not stripped:
        return False

    if len(stripped) == 0:
        return False

    for i, c in enumerate(stripped):
        isLast = i == (len(stripped) - 1) # is symbol in the end of string
        isFirst = i == 0 # is symbol in the begin of string
        if isFirst:
            # Check if symbol is allowd in the begin of string
            listFirst = list(map(str, range(0,10)))
            if not c in listFirst:
                return False
        elif isLast:
            # Check if symbol is allowd in the end of string
            listLast = list(map(str, range(0,10))) + ['s', 'm', 'h', 'd', 'w', 'm', 'y']
            if not c in listLast:
                return False
        else:
            # Check if symbol is allowd in the middle of string
            listMiddle = list(map(str, range(0,10))) + ['.', ',']
            if not c in listMiddle:
                return False

    w = withoutQualifier(stripped)

    # Minimal allowed interval is 1s/1m/1h/1d/1w/1m/1y
    # TODO: allow intervals like 0.5m or 0.5h
    return float(w) >= 1

# If this file is launched (instead of including) run tests (for development purposes)
# TODO: move it into unit test
if __name__ == "__main__":
    stringsValid = [
        '1',
        '1 ',
        ' 1 ',
        '1.0',
        '1.0s',
        '1.01s',
        '5',
        '1s',
        '2m',
        '3.5h'
    ]

    stringsNonValid = [
        '',
        '0',
        '0s',
        '0.01s',
        '-1',
        '1z',
        'abc',
    ]

    for s in stringsValid:
        h = {'s': s, 'isStringValid(s)': isStringValid(s)}
        print('l20: ' + str(h))

    for s in stringsNonValid:
        h = {'s': s, 'isStringValid(s)': isStringValid(s)}
        print('l29: ' + str(h))

    print(withoutQualifier('0s'))
