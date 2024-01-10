from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

from service.api.models import DBPrediction

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

class SignInResponse(BaseModel):
    access_token: str
    user_info: User

class PredictionResult(BaseModel):
    datetime: datetime
    is_anomaly: bool
    anomaly_probability: float
        


class PredictionResponse(BaseModel):
    prediction_id: int
    prediction_model_id: int
    created_at: datetime
    prediction_results: Optional[List[PredictionResult]]
    error_info: Optional[str]

    @classmethod
    def from_db_prediction(cls, db_prediction: DBPrediction):

        data_dict = db_prediction.output_data

        if data_dict is None:
            results = None
        else:
            results = [PredictionResult(datetime=datetime.fromisoformat(dt), is_anomaly=bool(ia), anomaly_probability=ap) 
                       for dt, ia, ap in zip(data_dict["timestamp"].values(),
                                             data_dict["anomaly_prediction"].values(),
                                             data_dict["anomaly_proba"].values())]

        responce = PredictionResponse(prediction_id = db_prediction.id,
                                      prediction_model_id=db_prediction.predictor_id,
                                      created_at=db_prediction.created_at,
                                      prediction_results=results,
                                      error_info=db_prediction.error_info)
    
        return responce


class PredictiorInfo(BaseModel):
    id: int
    name: str
    filename: str
    cost: int
    is_active: bool
