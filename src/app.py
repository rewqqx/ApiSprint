from fastapi import FastAPI

from src.api.base_router import router

tags_dict = [
    {
        'name': 'tanks',
        'description': 'Резервуар',
    },
    {
        'name': 'operations',
        'description': 'Операция',
    },
    {
        'name': 'products',
        'description': 'Продукт',
    },
    {
        'name': 'users',
        'description': 'Пользователь',
    },
]

app = FastAPI(
    title='Sprint Task',
    description='This is my sprint task',
    version='0.0.1',
)

app.include_router(router)
