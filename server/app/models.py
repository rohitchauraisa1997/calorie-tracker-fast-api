'''
defines models used for serving the backend
'''
import json
import datetime
from typing import Optional
from pydantic import BaseModel, validator, Field


class CustomJSONEncoder(json.JSONEncoder):
    '''
    used for converting the datetime objects to str
    ensures that when we entry objects as response
    we dont get error.
    '''
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)


class Entry(BaseModel):
    '''
    Entry class represents each entry in the mongo collection.
    '''
    dish: str
    size: Optional[int]
    ingredients: Optional[str]
    proteins: Optional[int]
    carbs: Optional[int]
    fat: Optional[int]
    calories: Optional[int]
    created_at: Optional[datetime.datetime] = Field(alias="createdAt", default=None)
    updated_at: Optional[datetime.datetime] = Field(alias="updatedAt", default=None)
    soft_deleted_at: Optional[datetime.datetime] = Field(
        alias="softDeletedAt", default=None
    )

    def __post_init__(self):
        '''
        this function helps in converting python's snake case to 
        pascal case while we are adding docs to the mongo collection.
        if this method is not there the docs added to mongo collection 
        will have "created_at", "updated_at", "soft_deleted_at" params
        instead of "createdAt", "updatedAt", "softDeletedAt".
        '''
        self.created_at = self.createdAt
        self.updated_at = self.updatedAt
        self.soft_deleted_at = self.softDeletedAt

    @classmethod
    @validator("dish")
    def title_must_not_be_blank(cls, value):
        '''
        validation check example
        '''
        if not value.strip():
            raise ValueError("Dish must not be blank")
        return value

    def to_json(self):
        '''
        helps convert the entry entity to json response.
        '''
        return json.dumps(self.dict(), ensure_ascii=False, cls=CustomJSONEncoder)
