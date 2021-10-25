from .simple_model import SimpleModel

class MostPopular(SimpleModel):
    '''Selecciona la ordenación más popular.'''

    def distance(self, calendar1, calendar2):
        return -1 if calendar1 == calendar2 else 0

    def merge(self, d1, d2):
        return d1 + d2