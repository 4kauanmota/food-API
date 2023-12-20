from pydantic import BaseModel, Field
from typing import Optional 
from itertools import count

c = count()

class Food(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(c))
    name: str
    color: str
    
class FoodQuery(BaseModel):
    id: Optional[int]
    name: Optional[str]
    color: Optional[str]
    
class Foods(BaseModel):
    foods: list[Food]
    count: int