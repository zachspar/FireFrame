"""
FireFrame core CRUD views.
"""
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
        setattr(self, "prefix", f"/{self.serializer_class.Meta.model.Meta.collection_name}")
        setattr(self, "tags", [self.serializer_class.Meta.model.__name__])
        super().__init__()
        self._generate_routes()

    def _generate_routes(self):
        # Create the FastAPI router with the defined endpoints
        @self.get(path="/")
        async def get_all() -> list[BaseReadAPIView.serializer_class]:
            # Retrieve all objects from the model
            objects = self.serializer_class.Meta.model.objects.all()

            # Serialize the objects
            serialized_data = [self.serializer_class.from_model(obj).model_dump() for obj in objects]

            return serialized_data

        @self.get("/{id}", response_model=self.serializer_class)
        async def get_by_id(id: str):
            # Retrieve the object with the specified ID
            try:
                obj = self.serializer_class.Meta.model.objects.get(id=id)
            except ReferenceDocNotExist:
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
