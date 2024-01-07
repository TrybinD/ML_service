from service.api.repositories.base import SQLAlchemyRepository
from service.api.models import DBPrediction

class PredictionRepository(SQLAlchemyRepository):
    model = DBPrediction