from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.operation import Operation
from src.models.schemas.operation.operation_request import OperationRequest
import csv
from io import StringIO
from datetime import datetime


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Operation]:
        operations = (
            self.session
            .query(Operation)
            .order_by(
                Operation.id.desc())
            .all()
        )

        return operations

    def get(self, operation_id: int) -> Operation:
        operation = (
            self.session
            .query(Operation)
            .filter(
                Operation.id == operation_id,
            )
            .first()
        )
        return operation

    def get_by_tank(self, tank_id: int) -> List[Operation]:
        operations = (
            self.session
            .query(Operation)
            .filter(
                Operation.tank_id == tank_id
            )
            .order_by(
                Operation.id.desc())
            .all()
        )

        return operations

    def add(self, user_id: int, operation_schema: OperationRequest) -> Operation:
        operation_dict = operation_schema.dict()
        operation_dict['created_by'] = user_id
        operation_dict['modified_by'] = user_id
        operation = Operation(**operation_dict)
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, user_id: int, operation_id: int, operation_schema: OperationRequest) -> Operation:
        operation = self.get(operation_id)
        for field, value in operation_schema:
            setattr(operation, field, value)
        setattr(operation, 'modified_by', user_id)
        self.session.commit()
        return operation

    def delete(self, operation_id: int):
        operation = self.get(operation_id)
        self.session.delete(operation)
        self.session.commit()

    def get_tid_pid_ds_de(self, tank_id: int, product_id: int, date_start: datetime, date_end: datetime):
        operations = (
            self.session
            .query(Operation)
            .filter(
                Operation.tank_id == tank_id
            )
            .filter(
                Operation.product_id == product_id
            )
            .filter(
                Operation.date_start >= date_start
            )
            .filter(
                Operation.date_end <= date_end
            )
            .order_by(
                Operation.id.desc())
            .all()
        )

        return operations
