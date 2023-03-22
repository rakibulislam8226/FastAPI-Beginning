from fastapi import FastAPI
from enum import Enum
from typing import Union
from pydantic import BaseModel

app = FastAPI()


@app.get("/", description="For home.")
def home():
    return {"message": "This one is from home."}


@app.post("/")
async def read_root():
    return {"Hello": "World"}


# @app.get("/items")
# async def items():
#     return {"message": "List items"}


@app.get("/item/{item_id}")
async def get_item_list(item_int):
    return {"Item nummber": item_int}


class Food(str, Enum):
    food = 'food'
    cricket = 'cricket'
    work = 'work'


@app.get('/food/{food_name}')
async def food_list(food_name: Food):
    if food_name == Food.food:
        return {"message": "Healthy", "food_name": food_name}

    if food_name.cricket == 'cricket':
        return {"you don't like food you like": food_name.cricket}

    return {"Message": "you don't like anything."}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.get("/item_set/{item_id}/user_id/{user_id}")
async def read_item(item_id: str, user_id: Union[str, None] = None, q: Union[str, None] = None, short: bool = False):
    items = {"item_id": item_id, "user_id": user_id}
    if q:
        items.update({"q": q})
    if short is False:
        items.update({
            "message": "And of course, you can define some parame"
        })
        return items
    return items


class Model(BaseModel):
    name: str
    price: int
    is_offer: Union[bool, None] = None
    tax: Union[float, None] = None


@app.put("/model")
async def model_put(model: Model):
    total_price = model.price + model.tax
    model_dict = model.dict()
    if model.tax:
        model_dict.update({"price_with_tax": total_price})
    return model_dict
