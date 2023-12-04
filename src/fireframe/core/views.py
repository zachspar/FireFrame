"""
FireFrame core CRUD views.
"""
from typing import List

from fastapi import APIRouter, HTTPException
from fireo.queries.errors import ReferenceDocNotExist

from .serializers import ModelSerializer

__all__ = [
    "BaseAPIView",
    "BaseListAPIView",
    "BaseRetrieveAPIView",
    "BaseCreateAPIView",
    "BaseUpdateAPIView",
    "BaseDestroyAPIView",
]


class BaseAPIView(APIRouter):
    serializer_class = None

    def _generate_routes(self):
        raise NotImplementedError("Subclasses must implement _generate_routes")

    def __init__(self):
        super().__init__()
        if not issubclass(self.serializer_class, ModelSerializer):
            raise TypeError("serializer_class must be a subclass of ModelSerializer")
        self._generate_routes()

    @classmethod
    def as_router(cls):
        """
        Instantiate the view and return the router.
        """
        return cls()


class BaseListAPIView(BaseAPIView):
    def _generate_routes(self):
        self.add_api_route("/", self.list, response_model=List[self.serializer_class], methods=["GET"])

    async def list(self):
        """
        List all objects of the model.
        """
        # Retrieve all objects from the model
        objects = self.serializer_class.Meta.model.collection.fetch()

        # Serialize the objects
        serialized_data = [self.serializer_class.from_model(obj).model_dump() for obj in objects]

        return serialized_data


class BaseRetrieveAPIView(BaseAPIView):
    def _generate_routes(self):
        self.add_api_route("/{id}", self.retrieve, response_model=self.serializer_class, methods=["GET"])

    async def retrieve(self, id: str):
        """
        Retrieve a single model object by ID.
        """
        try:
            obj = self.serializer_class.Meta.model.collection.get(id)
        except ReferenceDocNotExist:
            raise HTTPException(status_code=404, detail=f"{self.serializer_class.Meta.model.__name__} not found.")

        if obj is None:
            raise HTTPException(status_code=404, detail=f"{self.serializer_class.Meta.model.__name__} not found.")

        # Serialize the object
        serialized_data = self.serializer_class.from_model(obj).model_dump()

        return serialized_data


class BaseCreateAPIView(BaseAPIView):
    def _generate_routes(self):
        # NOTE: annotations hack to add type annotations to the create function dynamically
        self.create.__annotations__["serializer_data"] = self.serializer_class
        self.add_api_route("/", self.create, response_model=self.serializer_class, methods=["POST"])

    async def create(self, serializer_data):
        """
        Create a new model object.
        """
        # Convert the serializer to a model instance
        model = self.serializer_class.to_model(serializer_data)

        # Save the model instance
        model.save()

        # Serialize the model instance
        serialized_data = self.serializer_class.from_model(model).model_dump()

        return serialized_data


class BaseUpdateAPIView(BaseAPIView):
    def _generate_routes(self):
        # NOTE: annotations hack to add type annotations to the update function dynamically
        self.update.__annotations__["serializer_data"] = self.serializer_class
        self.add_api_route("/{id}", self.update, response_model=self.serializer_class, methods=["PUT"])

    async def update(self, id: str, serializer_data):  # TODO FIXME serializer_data: self.serializer_class
        """
        Update a model object by ID.
        """
        try:
            obj = self.serializer_class.Meta.model.collection.get(id)
        except ReferenceDocNotExist:
            raise HTTPException(status_code=404, detail=f"{self.serializer_class.Meta.model.__name__} not found.")

        if obj is None:
            raise HTTPException(status_code=404, detail=f"{self.serializer_class.Meta.model.__name__} not found.")

        # set all attributes of the object to the new values
        for field, value in serializer_data.model_dump().items():
            setattr(obj, field, value)

        # save the object
        obj.save(merge=True)

        # Serialize the model instance
        serialized_data = self.serializer_class.from_model(obj).model_dump()

        return serialized_data


class BaseDestroyAPIView(BaseAPIView):
    def _generate_routes(self):
        self.add_api_route("/{id}", self.destroy, methods=["DELETE"])

    async def destroy(self, id: str) -> None:
        """
        Delete a model object by ID.
        """
        self.serializer_class.Meta.model.collection.delete(id, child=True)
