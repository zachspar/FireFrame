"""
FireFrame core CRUD views.
"""
from typing import List

from fastapi import APIRouter, HTTPException
from fireo.queries.errors import ReferenceDocNotExist

from .serializers import ModelSerializer


__all__ = [
    "BaseReadAPIView",
]


class BaseReadAPIView(APIRouter):
    serializer_class = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not issubclass(cls.serializer_class, ModelSerializer):
            raise TypeError("serializer_class must be a subclass of ModelSerializer")

    def __init__(self):
        super().__init__()
        self._generate_routes()

    def _generate_routes(self):
        self.add_api_route("/", self.get_all, response_model=List[self.serializer_class])
        self.add_api_route("/{id}", self.get_by_id, response_model=self.serializer_class)

    async def get_all(self):
        # Retrieve all objects from the model
        objects = self.serializer_class.Meta.model.collection.fetch()

        # Serialize the objects
        serialized_data = [self.serializer_class.from_model(obj).model_dump() for obj in objects]

        return serialized_data

    async def get_by_id(self, id: str):
        # Retrieve the object with the specified ID
        try:
            obj = self.serializer_class.Meta.model.collection.get(id)
        except ReferenceDocNotExist:
            raise HTTPException(status_code=404, detail="Object not found")

        if obj is None:
            raise HTTPException(status_code=404, detail="Object not found")

        # Serialize the object
        serialized_data = self.serializer_class.from_model(obj).model_dump()

        return serialized_data

    @classmethod
    def as_router(cls):
        """
        Instantiate the view and return the router.
        """
        return cls()
