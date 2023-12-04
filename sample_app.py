"""A sample FireFrame API."""
from fireframe.core.api import *
from fireframe.core.models import *
from fireframe.core.serializers import *
from fireframe.core.views import *


class User(Model):
    """
    User model.

    Inherits from FireFrame's Model.
    """

    class Meta:
        collection_name = "users_sample_collection"

    name: str
    email: str
    age: int


class UserSerializer(ModelSerializer):
    """
    User serializer.

    Inherits from FireFrame's ModelSerializer.
    """

    class Meta:
        model = User
        fields = ["name", "email", "age"]


class UserListAPI(BaseListAPIView):
    serializer_class = UserSerializer


class UserRetrieveAPI(BaseRetrieveAPIView):
    serializer_class = UserSerializer


class UserCreateAPI(BaseCreateAPIView):
    serializer_class = UserSerializer


class UserUpdateAPI(BaseUpdateAPIView):
    serializer_class = UserSerializer


class UserDestroyAPI(BaseDestroyAPIView):
    serializer_class = UserSerializer


app = FireFrameAPI(title="Sample FireFrame App", version="0.0.0")
app.include_router(UserListAPI.as_router())
app.include_router(UserRetrieveAPI.as_router())
app.include_router(UserCreateAPI.as_router())
app.include_router(UserUpdateAPI.as_router())
app.include_router(UserDestroyAPI.as_router())
