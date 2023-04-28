from typing import Annotated, Any

from fastapi import Body, Cookie, FastAPI, Header
from pydantic import BaseModel, EmailStr, Field, HttpUrl

new_app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0, description="The price must be greater than zero"
    )
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@new_app.post("offers/")
async def create_offer(offer: Offer):
    return offer


@new_app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results


@new_app.get("/items/")
async def read_items(
    ads_id: Annotated[str | None, Cookie(example="skyfr")] = None
):
    return {"ads_id": ads_id}


@new_app.get("/items/one/")
async def read_items_one(
    strange_header: Annotated[str | None, Header()] = None
):
    return {"strange_header": strange_header}


@new_app.get("/items/two/")
async def read_items_two(
    x_token: Annotated[list[str] | None, Header()] = None
):
    return {"X-Token values": x_token}


@new_app.post("/items/three/", response_model=Item)
async def create_item_three(item: Item) -> Any:
    return item


@new_app.get("/items/four/", response_model=list[Item])
async def read_items_four() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


@new_app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user


# async def get_db():
#     db = DBSession()
#     try:
#         yield db
#     finally:
#         db.close()
