from fastapi import FastAPI
from enum import Enum


app = FastAPI()

@app.get("/", description="For home.")
def home():
    return {"message": "This one is from home."}


@app.post("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items")
async def items():
    return {"message": "List items"}


@app.get("/items/{item_id}")
async def get_item_list(item_int):
    return {"Item nummber": item_int}


class Food(str, Enum):
    food = 'food'
    cricket = 'cricket'

@app.get('/food/{food_name}')
async def food_list(food_name:Food):
    if food_name == Food.food:
        return {"message": "Healthy", "food_name": food_name}
    
    if food_name.cricket == 'cricket':
        return {"you don't like food you like":food_name.cricket}
    
    return {"Message":"you don't like anything."}
