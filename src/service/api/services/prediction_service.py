from typing import Optional
from pathlib import Path

from fastapi import HTTPException
import pandas as pd

from service.api.repositories.base import AbstractRepository
from service.api.repositories.prediction_repo import PredictionRepository
from service.api.repositories.predictor_repo import PredictorRepository
from service.api.repositories.user_repo import UserRepository
from service.api.tasks.make_prediction import run_model_inference


class PredictionService:
    def __init__(self,
                 prediction_repo: AbstractRepository, 
                 predictior_repo: AbstractRepository,
                 user_repo: AbstractRepository):
        self.prediction_repo: AbstractRepository = prediction_repo()
        self.predictior_repo: AbstractRepository = predictior_repo()
        self.user_repo: AbstractRepository = user_repo()

    async def register_prediction(self, user_id: int, model: str, **kwargs):

        db_predictor = await self.predictior_repo.find_by_options(name=model, unique=True)
        db_user = await self.user_repo.find_by_options(id=user_id, unique=True)

        if db_predictor is None:
            raise HTTPException(status_code=404, detail="Predictor not found")
        
        if db_user.balance < db_predictor.cost:
            raise HTTPException(status_code=400, detail="Not enough balance")
        
        await self.user_repo.update({"balance": db_user.balance - db_predictor.cost}, id=user_id)
        
        prediction_data = {}
        prediction_data["predictor_id"] = db_predictor.id
        prediction_data["user_id"] = user_id

        if "file" in kwargs:
            prediction_data["input_data_type"] = "file"
        elif "start_datetime" in kwargs and "end_datetime" in kwargs:
            prediction_data["input_data_type"] = "db"
            prediction_data["start_datetime"] = kwargs["start_datetime"]
            prediction_data["end_datetime"] = kwargs["end_datetime"]

        prediction_id = await self.prediction_repo.add(data=prediction_data)

        if "file" in kwargs:
            data_filename = str(prediction_id) + ".csv"

            df = pd.read_csv(kwargs["file"].file)
            df.to_csv(Path("data/temp") / data_filename, index=False)
            
            kwargs["file"] = str(Path("data/temp") / data_filename)

        run_model_inference.delay(prediction_id, db_predictor.filename, db_predictor.cost, db_user.id, db_user.balance, **kwargs)            

        return prediction_id

    async def get_predictions(self, user_id: int, prediction_id: Optional[int] = None,
                              only_finished=False, only_succeed=False):

        kwargs = {}
        if only_finished:
            kwargs["is_finished"] = True
        
        if only_succeed:
            kwargs["is_success"] = True

        if prediction_id is None:
            predictions = await self.prediction_repo.find_by_options(user_id=user_id)
        else:
            predictions = await self.prediction_repo.find_by_options(id=prediction_id, 
                                                                     user_id=user_id, 
                                                                     unique=True)
        return predictions
    
def prediction_service():
    return PredictionService(prediction_repo=PredictionRepository,
                             predictior_repo=PredictorRepository,
                             user_repo=UserRepository)