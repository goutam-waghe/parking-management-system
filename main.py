from typing import Union

from fastapi import FastAPI

app = FastAPI()


def new_feature():
    print("new feature")

def anither_feature():
    print("another feature")
    
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/items")
def read_item():
    return {
        "message":"your all items"
    }