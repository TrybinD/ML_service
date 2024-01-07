from pathlib import Path
from datetime import datetime
from time import sleep
import asyncio
import random

import pandas as pd
from celery import Celery

from models.base_model import AbstractModel
from service.api.repositories.prediction_repo import PredictionRepository
from service.api.repositories.user_repo import UserRepository

MODELS_PATH = Path("models")

celery = Celery("prediction_tasks", broker="redis://localhost:6379")

@celery.task
def run_model_inference(prediction_id, model_filename, model_cost, user_id, user_balance, **kwargs):

    try:
        model: AbstractModel = AbstractModel.load(MODELS_PATH / Path(model_filename))

        if "file" in kwargs:
            data = pd.read_csv(kwargs["file"], parse_dates=["timestamp"])
        elif "start_datetime" in kwargs and "end_datetime" in kwargs:
            data = pd.read_csv(Path("data/database_gas.csv"), parse_dates=["timestamp"])
            data["timestamp"] = pd.to_datetime(data.timestamp).dt.tz_localize(None)
            data = data[(data["timestamp"] >= str(kwargs["start_datetime"])) & (data["timestamp"] <= kwargs["end_datetime"])]

        df_anomaly = model.predict(data=data)
        df_proba = model.predict_proba(data=data)

        if random.random() < 0.1:
            raise Exception("Some error")

        sleep(20)

        df = df_anomaly.merge(df_proba)

        df["timestamp"] = df["timestamp"].astype(str)
        
        result = df.to_dict()

        data_to_update = {"predicted_at": datetime.now(),
                          "is_success": True,
                          "is_finished": True,
                          "output_data": result}
    
    except Exception as e:
        print(e)

        asyncio.run(UserRepository().update(data={"balance": user_balance}, id=user_id))

        data_to_update = {"predicted_at": datetime.now(),
                          "is_success": False,
                          "is_finished": True,
                          "error_info": str(e)}
    
    asyncio.run(PredictionRepository().update(data=data_to_update, id=prediction_id))
