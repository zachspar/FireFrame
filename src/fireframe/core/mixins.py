"""
Commonly used FireFrame mixins.
"""
from fastapi import APIRouter
from .views import *


__all__ = [
    "crud_router",
]


class BaseAPIViewSet(BaseAPIView):
    """
    Base viewset.
    """


def crud_router(input_serializer_class):
    router = APIRouter()

    class CreateView(BaseCreateAPIView):
        serializer_class = input_serializer_class

    class RetrieveView(BaseRetrieveAPIView):
        serializer_class = input_serializer_class

    class UpdateView(BaseUpdateAPIView):
        serializer_class = input_serializer_class

    class DestroyView(BaseDestroyAPIView):
        serializer_class = input_serializer_class

    router.include_router(CreateView.as_router())
    router.include_router(RetrieveView.as_router())
    router.include_router(UpdateView.as_router())
    router.include_router(DestroyView.as_router())
    return router
