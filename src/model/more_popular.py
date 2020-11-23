from .base import BaseModel

class MostPopular(BaseModel):
    '''Selecciona el calendario más popular'''

    def distance(self, calendar1, calendar2):
        return -1 if calendar1 == calendar2 else 0

    def merge(self, d1, d2):
        return d1 + d2