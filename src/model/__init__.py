from .base import ModelError
from .model import Positions

def use_model(data, model_name=None):
    '''
    Find a model with name `model_name` and 
    return the solution of eval data
    '''
    if model_name is None:
        model_name = defaul_model
    for model in models:
        if model.__name__.lower() == model_name.lower():
            return model().solve(data)
    raise ModelError('Model not found')


defaul_model = Positions.__name__

models = [
    Positions,
]