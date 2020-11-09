from .utils import next_permutation

class ModelError(Exception):
    pass

class BaseModel:
    '''
    Base class to implement a calendar selector model
    '''
    def __init__(self, null=0):
        self.null = null

    def solve(self, data:list):
        '''
        Given a data set of option
        find the distribution that
        minimice the sumatory of 
        inversions with every option
        '''
        if not data:
            return None
        dis, solution = float('inf'), None
        cur = data[0].copy()
        cur.sort()
        while True:
            value = self.f(cur, data)
            if value < dis:
                dis, solution = value, cur.copy()
            if not next_permutation(cur):
                break
        return solution

    def f(self, calendar:list, data:list):
        '''
        Given a calendar and a list of proposals
        find the merged distances value to all of them
        '''
        value = self.null
        for propose in data:
            value = self.merge(value, self.distance(calendar, propose))
        return value

    def valid(self, calendar1, calendar2):
        '''
        Check if the given calendars has the same elements, and 
        every element has a unique occurrence 
        '''
        order1, order2 = calendar1.copy(), calendar2.copy()
        order1.sort()
        order2.sort()
        for i in range(1, len(order1)):
            if order1[i] == order1[i - 1]:
                raise ModelError('Duplicated elements')

        if order1 != order2:
            raise ModelError('Malformed query')
        
    def merge(self, d1:int, d2:int):
        '''
        Return the composite value of two distance values
        '''
        pass

    def distance(self, calendar1, calendar2):
        '''
        Return a value that describes the difference between two calendars
        '''
        pass

