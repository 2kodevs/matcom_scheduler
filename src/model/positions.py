from .simple_model import SimpleModel

class Positions(SimpleModel):
    '''Selecciona la ordenación que minimice la suma de la cantidad de permutaciones requeridas por cada voto para alcanzar dicha ordenación.'''

    def distance(self, calendar1:list, calendar2:list):
        '''
        Return the number of inversions
        necessary to transform calendar1 in calendar2
        <param> calendar1 - list of data
        <param> calendar2 - list of data
        <return> int - Number of inversions
        '''
        self.valid(calendar1, calendar2)
        
        d, inv = {}, 0
        for (i, item) in enumerate(calendar1):
            d[item] = i
        for (i, item) in enumerate(calendar2):
            inv += abs(i - d[item])
        return inv

    def merge(self, d1, d2):
        return d1 + d2
