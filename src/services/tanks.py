from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.tank import Tank
from src.models.schemas.tank.tank_request import TankRequest


class TanksService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Tank]:
        tanks = (
            self.session
            .query(Tank)
            .order_by(
                Tank.id.desc()
            )
            .all()
        )
        return tanks

    def get(self, tank_id: int) -> Tank:
        tank = (
            self.session
            .query(Tank)
            .filter(
                Tank.id == tank_id,
            )
            .first()
        )
        return tank

    def change_current_capacity(self, user_id: int, tank_id: int, current_capacity: int):
        tank = self.get(tank_id)
        setattr(tank, 'current_capacity', current_capacity)
        setattr(tank, 'modified_by', user_id)
        self.session.commit()
        return tank

    def add(self, user_id: int, tank_schema: TankRequest) -> Tank:
        tank_dict = tank_schema.dict()
        tank_dict['created_by'] = user_id
        tank_dict['modified_by'] = user_id
        tank = Tank(**tank_dict)
        self.session.add(tank)
        self.session.commit()
        return tank

    def update(self, user_id: int, tank_id: int, tank_schema: TankRequest) -> Tank:
        tank = self.get(tank_id)
        for field, value in tank_schema:
            setattr(tank, field, value)
        setattr(tank, 'modified_by', user_id)
        self.session.commit()
        return tank

    def delete(self, tank_id: int):
        tank = self.get(tank_id)
        self.session.delete(tank)
        self.session.commit()
