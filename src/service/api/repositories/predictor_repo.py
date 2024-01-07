from service.api.repositories.base import SQLAlchemyRepository
from service.api.models import DBPredictor

class PredictorRepository(SQLAlchemyRepository):
    model = DBPredictor
