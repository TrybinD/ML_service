from fastapi import APIRouter, Depends

from service.api.schemas import PredictiorInfo
from service.api.security import check_dev_key
from service.api.repositories.predictor_repo import PredictorRepository


router = APIRouter(prefix="/dev", tags=["dev"], dependencies=[Depends(check_dev_key)])


@router.post("/add-model")
async def add_model(predictor_info: PredictiorInfo) -> int:
    predictor_info = predictor_info.model_dump()

    predictor_id = await PredictorRepository().add(predictor_info)

    return predictor_id
