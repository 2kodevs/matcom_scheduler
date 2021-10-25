from .base import BaseModel


class Score(BaseModel):
    '''Ordena las opciones según la cantidad de puntos alcanzados por cada una. Cada votante asigna una determinada cantidad de puntos a cada opción, de acuerdo con la posición que le otorgó en la lista al votar.'''
    def solve(self, data: list):
        sample = data[0]
        N = len(sample)
        scores: dict = dict()
        for op in sample:
            scores[op] = 0

        for vote in data:
            for index, option in enumerate(vote):
                option_score = N + 1 - (index + 1)
                try:
                    scores[option] += option_score
                except KeyError:
                    scores[option] = option_score
        
        result = [(score, option) for option, score in scores.items()]
        result.sort(reverse=True)
        return result
