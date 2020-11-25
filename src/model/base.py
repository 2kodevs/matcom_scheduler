class ModelError(Exception):
    pass

class BaseModel:
    '''Base class to implement a calendar selector model'''

    def __call__(self, data:list):
        if not data:
            return None
        return self.solve(data)

    def solve(self, data:list):
        '''
        Given a data set of option
        returns an order that satisfy 
        the expected consensus 
        '''
        raise ModelError("`Solve` function not implemented")
