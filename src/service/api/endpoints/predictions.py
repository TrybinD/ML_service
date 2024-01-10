from typing import List, Annotated
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Depends

from service.api.schemas import PredictionResponse, PredictionResult, User
from service.api.security import get_current_user
from service.api.services.prediction_service import prediction_service, PredictionService


router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("/from-file/{model}")
async def create_prediction_from_file(model: str, 
                                      prediction_service: Annotated[PredictionService, Depends(prediction_service)],
                                      file: UploadFile = File(...),
                                      user: User = Depends(get_current_user)) -> int:
    """Create prediction task to determinate hours in file is normal or anomaly"""
    # TODO: add validation for columns and datetimes

    prediction_id = await prediction_service.register_prediction(user_id=user.id, model=model, file=file)
    return prediction_id

@router.post("/by-date/{model}")
async def create_prediction_from_data(model: str, 
                                      start_datetime: str, 
                                      end_datetime: str,
                                      prediction_service: Annotated[PredictionService, Depends(prediction_service)],
                                      user: User = Depends(get_current_user)) -> int:
    """Create prediction task to determinate hours in period form start_datetime to end_datetime is normal or anomaly"""

    prediction_id = await prediction_service.register_prediction(user_id=user.id, 
                                                                 model=model,
                                                                 start_datetime=datetime.strptime(start_datetime, "%Y-%m-%d %H:%M"),
                                                                 end_datetime=datetime.strptime(end_datetime, "%Y-%m-%d %H:%M"))
    return prediction_id

@router.get("/{prediction_id}")
async def get_prediction_by_id(prediction_id: int, 
                               prediction_service: Annotated[PredictionService, Depends(prediction_service)],
                               user: User = Depends(get_current_user)) -> PredictionResponse:
    """Get predictions from DB by prediction_id"""

    prediction = await prediction_service.get_predictions(user_id=user.id, 
                                                          prediction_id=prediction_id)


    responce = PredictionResponse.from_db_prediction(prediction)
    
    return responce

@router.get("/")
async def get_prediction_all(prediction_service: Annotated[PredictionService, Depends(prediction_service)],
                             user: User = Depends(get_current_user),
                             only_finished: bool = False,
                             only_succeed: bool = False) -> List[PredictionResponse]:
    """Get all predictions from DB to given user"""

    predictions = await prediction_service.get_predictions(user_id=user.id, 
                                                           only_finished=only_finished, 
                                                           only_succeed=only_succeed)

    responces = [PredictionResponse.from_db_prediction(prediction) for prediction in predictions]
    
    return responces
