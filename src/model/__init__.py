from .score import Score
from .base import ModelError
from .positions import Positions
from .minimun import Minimum
from .most_popular import MostPopular
from .dea_ar_model import DEA_AR

def use_model(data, model_name=None):
    '''
    Find a model with name `model_name` and 
    return the solution of eval data
    '''
    if model_name is None:
        model_name = default_model
    for model in models:
        if model.__name__.lower() == model_name.lower():
            return model()(data)
    raise ModelError('Model not found')


default_model = Score.__name__

models = [
    DEA_AR,
    Positions,
    Minimum,
    MostPopular,
    Score,
]