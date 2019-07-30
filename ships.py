
class Spaceship:

    def __init__(self):
        self.location = None
        self.artifacts = 0
        self.cargo = ''
        self.active = True

    def move_to(self, planet):
        self.location = planet

    def get_report(self):
        result = '''
Spaceship Bridge
================
cargo              : %s
artifacts found    : %i/5
''' % (self.cargo, self.artifacts)
        return result

    def __repr__(self):
        return f"<spaceship at: {self.location.name}>"
