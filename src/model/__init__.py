from .base import ModelError
from .model import Positions

def use_model(model_name, data):
    '''
    Find a model with name `model_name` and 
    return the solution of eval data
    '''
    for model in models:
        if model.__name__.lower() == model_name.lower():
            return model().solve(data)
    raise ModelError('Model not found')

models = [
    Positions,
]