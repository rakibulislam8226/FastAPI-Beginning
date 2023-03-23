from fastapi import FastAPI, Body, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# This will create our database if it doesn't already exists.
Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def getItems(session=Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.post("/")
async def addItem(item: schemas.Item, session=Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/{id}")
async def getItem(id: int, session=Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item


@app.put("/")
async def updateItem(id: int, item: schemas.Item, session=Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject


@app.delete("/id")
async def deleteItem(id: int, session=Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted.'


# fakedatabse = {
#     1: {'task1': "clear the task1"},
#     2: {'task2': "clear the task2"},
#     3: {'task3': "clear the task3"}
# }
#
#
# @app.get("/{id}")
# def getItems(id: int):
#     return fakedatabse[id]


# option 1
# @app.post("/")
# async def addItem(task: str):
#     newID = len(fakedatabse.keys()) + 1
#     fakedatabse[newID] = {"task": task}
#     return fakedatabse

# option 2
# @app.post("/")
# async def addItemSchemas(item: schemas.Item):
#     newId = len(fakedatabse.keys()) + 1
#     fakedatabse[newId] = {"task": item.task}
#     return fakedatabse
#
#
# @app.put("/{id}")
# async def updateItem(id: int, item: schemas.Item):
#     fakedatabse[id]["task"] = item.task
#     return fakedatabse
#
#
# @app.delete("/{id}")
# async def deleteItem(id: int):
#     del fakedatabse[id]
#     return fakedatabse
