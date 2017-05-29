
class Spaceship:

    def __init__(self):
        self.location = None
        self.artifacts = 0
        self.cargo = ''
        self.active = True

    def get_report(self):
        result = '''
Spaceship Bridge
================
cargo              : %s
artifacts found    : %i/5
''' % (self.cargo, self.artifacts)
        return result
