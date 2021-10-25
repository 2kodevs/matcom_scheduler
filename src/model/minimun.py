from .positions import Positions

class Minimum(Positions):
    '''Busca la ordenación que minimice la máxima cantidad de cambios de orden con respecto a las propuestas'''
    
    def merge(self, d1, d2):
        return max(d1, d2)
