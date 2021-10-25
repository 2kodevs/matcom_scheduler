from .base import BaseModel


class Score(BaseModel):
    '''Obtiene la ordenación según los puntos alcanzados por cada opción. Los puntos son de acuerdo al lugar que tuvo dicha opción en cada voto.'''
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
