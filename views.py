
SKIP_INPUT = False
SLOW_MOTION = False


def wait_for_input():
    if not SKIP_INPUT:
        input()


def wordwrap(lines):
    result = []
    for line in lines:
        while len(line) > 35:
            i = 34
            while i > 0 and line[i] != ' ':
                i -= 1
            if i == 0:
                i = len(line)
            result.append(line[:i].strip())
            line = line[i:].strip()
        result.append(line)
    return result

def print_twocolumn(r1, r2):
    r1 = wordwrap(r1.split('\n'))
    r2 = wordwrap(r2.split('\n'))
    ldiff = len(r1) - len(r2)
    if ldiff < 0:
        r1 += [''] * (-ldiff)
    elif ldiff > 0:
        r2 += [''] * ldiff
    for line1, line2 in zip(r1, r2):
        print("%-35s     %-35s"%(line1, line2))



def intro():
    print('''
This is the journey of the spaceship Controller
on its quest to explore the depths of space
in search of the legendary planet Olympus.
''')

def outro():
    print('''
You collected all artifact pieces that open the hidden vault of the Olympus system. Finally your quest has reached its end.
''')
