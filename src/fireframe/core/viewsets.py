"""
Commonly used FireFrame mixins.
"""
from fastapi import APIRouter

from .views import *

__all__ = [
    "crud_viewset",
]


def crud_viewset(input_serializer_class):
    router = APIRouter()

    class CreateView(BaseCreateAPIView):
        serializer_class = input_serializer_class

    class RetrieveView(BaseRetrieveAPIView):
        serializer_class = input_serializer_class

    class UpdateView(BaseUpdateAPIView):
        serializer_class = input_serializer_class

    class DestroyView(BaseDestroyAPIView):
        serializer_class = input_serializer_class

    router.include_router(CreateView())
    router.include_router(RetrieveView())
    router.include_router(UpdateView())
    router.include_router(DestroyView())
    return router
