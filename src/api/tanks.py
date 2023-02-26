from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.models.schemas.tank.tank_request import TankRequest
from src.models.schemas.tank.tank_response import TankResponse
from src.services.tanks import TanksService
from src.services.users import get_current_user_id

router = APIRouter(
    prefix='/tanks',
    tags=['tanks']
)


@router.get('/all', response_model=List[TankResponse], name='Получить все резервуары')
def get(tanks_service: TanksService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Получить все резервуары
    """
    return tanks_service.all()


@router.get('/get/{tank_id}', response_model=TankResponse, name='Получить один резервуар')
def get(tank_id: int, tanks_service: TanksService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Получить один резервуар
    """
    return get_with_check(tank_id, tanks_service)


def get_with_check(tank_id: int, tanks_service: TanksService):
    result = tanks_service.get(tank_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Резервуар не найден')
    return result


@router.get('/get/current_capacity/{tank_id, current_capacity}', response_model=TankResponse,
            name='Изменить значение current_capacity у резервуара')
def change_current_capacity(tank_id: int, current_capacity: int, tanks_service: TanksService = Depends(),
                            user_id: int = Depends(get_current_user_id)):
    """
    Изменить значение current_capacity у резервуара
    """
    result = tanks_service.get(tank_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Резервуар не найден')
    return tanks_service.change_current_capacity(user_id, tank_id, current_capacity)


@router.post('/', response_model=TankResponse, status_code=status.HTTP_201_CREATED, name="Добавить резервуар")
def add(tank_schema: TankRequest, tanks_service: TanksService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Добавить резервуар
    """
    return tanks_service.add(user_id, tank_schema)


@router.put('/{tank_id}', response_model=TankResponse, name="Обновить информацию о резервуаре")
def put(tank_id: int, tank_schema: TankRequest, tanks_service: TanksService = Depends(),
        user_id: int = Depends(get_current_user_id)):
    """
    Обновить информацию о резервуаре
    """
    get_with_check(tank_id, tanks_service)
    return tanks_service.update(user_id, tank_id, tank_schema)


@router.delete('/{tank_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить резервуар')
def delete(tank_id: int, tanks_service: TanksService = Depends(), user_id: int = Depends(get_current_user_id)):
    """
    Удалить резервуар
    """
    get_with_check(tank_id, tanks_service)
    return tanks_service.delete(tank_id)
