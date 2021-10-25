from .positions import Positions

class Minimum(Positions):
    '''Selecciona la ordenación que minimice la máxima cantidad de permutaciones requeridas por los votos para alcanzar dicha ordenación.'''
    
    def merge(self, d1, d2):
        return max(d1, d2)
