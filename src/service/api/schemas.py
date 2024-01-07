from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

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
    prediction_results: Optional[List[PredictionResult]]

    @classmethod
    def from_data_dict(cls, prediction_id:int, data_dict: dict):

        if data_dict is None:
            results = None
        else:
            results = [PredictionResult(datetime=datetime.fromisoformat(dt), is_anomaly=bool(ia), anomaly_probability=ap) 
                       for dt, ia, ap in zip(data_dict["timestamp"].values(),
                                             data_dict["anomaly_prediction"].values(),
                                             data_dict["anomaly_proba"].values())]

        responce = PredictionResponse(prediction_id = prediction_id,
                                      prediction_results=results)
    
        return responce


class PredictiorInfo(BaseModel):
    id: int
    name: str
    filename: str
    cost: int
    is_active: bool
