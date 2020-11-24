from .base import BaseModel

import numpy as np
from scipy.optimize import linprog

class DEA_AR(BaseModel):
    '''Busca el calendario más favorable según el modelo de exclusión DEA/AR(Data Envelopment Analysis/Assurance Region)'''
    
    def solve(self, data:list):
        if not data:
            return None

        t = len(data[0])
        e = 1 / t
        yrj = {element:[0]*t for element in data[0]}

        # fill yij
        for calendar in data:
            for i, x in enumerate(calendar):
                yrj[x][i] += 1

        # general model conditions
        ceros = [0]*t
        matrix, values = [], []
        for r in range(t - 1):
            matrix.append([*ceros[:r], -1, 1, *ceros[:t-(r+2)]])
            values.append(-e)
        for r in range(t - 2):
            matrix.append([*ceros[:r], -1, 2, -1, *ceros[:t-(r+3)]])
            values.append(0)
        matrix.append(ceros)
        matrix[-1][-1] = -1
        values.append(-e)   
        values.extend([1]*(t - 1))
        j = [[*yrj[element]] for element in data[0]]

        solved_data = []
        for element in data[0]:
            # objetive funtion
            c = np.array([-x for x in yrj[element]])

            # current conditions
            A = np.array([*matrix, *j[1:]])
            b = np.array(values)

            # using simplex to solve
            res = linprog(c, A_ub=A, b_ub=b)
            solved_data.append((res.fun, element))

            # rotate j to ensure the correct exclusion
            j.append(j.pop(0))
        solved_data.sort()
        return [x[1] for x in solved_data]
        