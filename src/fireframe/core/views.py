"""
FireFrame core CRUD views.
"""
from fastapi import APIRouter, HTTPException
from fireo.queries.errors import ReferenceDocNotExist
from pydantic import BaseModel as BaseSerialzer

from .serializers import ModelSerializer


class BaseReadAPIView(APIRouter):
    def __init__(self, serializer_class: BaseSerialzer):
        super().__init__()

        if not issubclass(serializer_class, ModelSerializer):
            raise TypeError("serializer_class must be a subclass of ModelSerializer")

        self.serializer_class = serializer_class

        @self.get("/")
        async def get_all(self):
            # Retrieve all objects from the model
            objects = serializer_class.Meta.model.objects.all()

            # Serialize the objects
            serialized_data = [serializer_class.from_model(obj).model_dump() for obj in objects]

            return serialized_data

        @self.get("/{id}", response_model=serializer_class)
        async def get_by_id(self, id: str):
            # Retrieve the object with the specified ID
            try:
                obj = serializer_class.Meta.model.objects.get(id=id)
            except ReferenceDocNotExist:
                raise HTTPException(status_code=404, detail="Object not found")

            # Serialize the object
            serialized_data = serializer_class.from_model(obj).model_dump()

            return serialized_data
