from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, ForeignKey, Float, JSON
from service.api.db import Base


class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    hash_password = Column(String(255), nullable=False)
    user_email = Column(String(255), nullable=False)
    balance = Column(Integer, default=500)


class DBPredictor(Base):
    __tablename__ = "predictor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    filename = Column(String(255), nullable=False, unique=True)
    cost = Column(Integer)
    is_active = Column(Boolean, default=True)


class DBPrediction(Base):
    __tablename__ = "prediction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    predicted_at = Column(DateTime(timezone=True), nullable=True, default=None)
    predictor_id = Column(Integer, ForeignKey("predictor.id"))
    input_data_type = Column(String(255))
    start_datetime = Column(DateTime, nullable=True, default=None)
    end_datetime = Column(DateTime, nullable=True, default=None)
    is_success = Column(Boolean, nullable=True, default=None)
    is_finished = Column(Boolean, nullable=False, default=False)
    output_data = Column(JSON, nullable=True)
    error_info = Column(String(255), nullable=True)
