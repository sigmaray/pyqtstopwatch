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

def doesEndWithQualifier(st):
    if not(st): return False
    if len(st) == 0: return False
    last = st[len(st) - 1]
    return last in ['s', 'm', 'h', 'd', 'w']

def withoutQualifier(st):    
    if (len(st) == 0): return st
    s = st.strip()    
    if (not(s)): return st
    if(not(doesEndWithQualifier(st))):
        return int(st)
    else:
        return int(st[:-1])

def getQualifierMult(st):    
    if (len(st) == 0): return 1
    s = st.strip()    
    if (not(s)): return 1
    if(not(doesEndWithQualifier(st))):
        return 1
    else:
        # return st[:-1]
        q = st[-1]
        
        if q == 's':
            return 1
        elif q == 'm':
            return 60
        elif q == 'h':
            return 60*60
        elif q == 'd':
            return 60*60*24
        elif q == 'w':
            return 60*60*24*7
        else:        
            return 1   # default

def isStringValid(st):
    s = st.strip()

    if not(s):
        return False

    if len(s) == 0:
        return False

    for i, c in enumerate(s):
        isLast = (i == len(s) - 1)
        isFirst = i == 0
        if isFirst:
            listFirst = list(map(str, range(0,10)))
            if (not(c in listFirst)):
                return False
        elif isLast:
            listLast = list(map(str, range(0,10))) + ['s', 'm', 'h', 'd', 'w', 'm', 'y']
            if (not(c in listLast)):
                return False
        else:
            listMiddle = list(map(str, range(0,10))) + ['.', ',']
            if (not(c in listMiddle)):
                return False

    w = withoutQualifier(s)

    return float(w) >= 1

# for s in stringsValid:
#     h = {'s': s, 'isStringValid(s)': isStringValid(s)}
#     print('l20: ' + str(h))

# for s in stringsNonValid:
#     h = {'s': s, 'isStringValid(s)': isStringValid(s)}
#     print('l29: ' + str(h))

# print(withoutQualifier('0s'))
