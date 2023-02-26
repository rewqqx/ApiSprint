from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.schemas.operation.operation_request import OperationRequest
from src.models.schemas.operation.operation_response import OperationResponse
from src.models.schemas.operation.operation_response_all import OperationResponseAll
from src.services.operations import OperationsService
from src.services.users import get_current_user_id
from datetime import datetime
from src.services.tanks import TanksService
from src.services.files import FilesService
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix='/operations',
    tags=['operations']
)


@router.get('/all', response_model=List[OperationResponseAll], name='Получить все операции')
def get(operations_service: OperationsService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Получить все операции
    """
    print(user_id)
    return operations_service.all()


@router.get('/get/{operation_id}', response_model=OperationResponse, name='Получить одну операцию')
def get(operation_id: int, operations_service: OperationsService = Depends(),
        user_id: int = Depends(get_current_user_id)):
    """
    Получить одну операцию
    """
    return get_with_check(operation_id, operations_service)


@router.get('/get/files/{tank_id, product_id, date_start, date_end}', name='Сформировать файл')
def get_file(tank_id: int, product_id: int, date_start: datetime, date_end: datetime,
             files_service: FilesService = Depends(), operations_service: OperationsService = Depends()):
    """
    Сформировать файл
    """
    operations = operations_service.get_tid_pid_ds_de(tank_id, product_id, date_start, date_end)
    report = files_service.download(operations)
    return StreamingResponse(report, media_type='text/csv',
                             headers={'Content-Disposition': 'attachment; filename=report.csv'})


@router.get('/get/tank/{tank_id}', response_model=List[OperationResponse], name='Получить одну операцию по tank_id')
def get_by_tank(tank_id: int, operations_service: OperationsService = Depends(), tank_service: TanksService = Depends(),
                user_id: int = Depends(get_current_user_id)):
    """
    Получить одну операцию
    """
    get_witch_check_tank(tank_id, tank_service)
    return operations_service.get_by_tank(tank_id)


def get_with_check(operation_id: int, operations_service: OperationsService):
    result = operations_service.get(operation_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Продукт не найден')
    return result


def get_witch_check_tank(tank_id: int, tank_service: TanksService):
    result = tank_service.get(tank_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Резервуар не найден')
    return result


@router.post('/', response_model=OperationResponse, status_code=status.HTTP_201_CREATED, name="Добавить операцию")
def add(operation_schema: OperationRequest, operations_service: OperationsService = Depends(),
        user_id: int = Depends(get_current_user_id)):
    """
    Добавить операцию
    """
    return operations_service.add(user_id, operation_schema)


@router.put('/{operation_id}', response_model=OperationResponse, name="Обновить информацию об операции")
def put(operation_id: int, operation_schema: OperationRequest, operations_service: OperationsService = Depends(),
        user_id: int = Depends(get_current_user_id)):
    """
    Обновить информацию об операции
    """
    get_with_check(operation_id, operations_service)
    return operations_service.update(user_id, operation_id, operation_schema)


@router.delete('/{operation_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить операцию')
def delete(operation_id: int, operations_service: OperationsService = Depends(),
           user_id: int = Depends(get_current_user_id)):
    """
    Удалить операцию
    """
    get_with_check(operation_id, operations_service)
    return operations_service.delete(operation_id)
