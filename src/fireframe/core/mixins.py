"""
Commonly used FireFrame mixins.
"""
from fastapi import APIRouter
from .views import *


__all__ = [
    "CrudMixin",
]


class BaseAPIViewSet(BaseAPIView):
    """
    Base viewset.
    """


class CrudMixin(BaseAPIViewSet):
    """
    Mixin for CRUD operations.
    """

    @classmethod
    def as_router(cls):
        """
        Instantiate a new router with CRUD views and return the router.
        """
        router = APIRouter()

        class CreateView(BaseCreateAPIView):
            serializer_class = cls.serializer_class

        class RetrieveView(BaseRetrieveAPIView):
            serializer_class = cls.serializer_class

        class UpdateView(BaseUpdateAPIView):
            serializer_class = cls.serializer_class

        class DestroyView(BaseDestroyAPIView):
            serializer_class = cls.serializer_class

        router.include_router(CreateView.as_router())
        router.include_router(RetrieveView.as_router())
        router.include_router(UpdateView.as_router())
        router.include_router(DestroyView.as_router())

        return router
