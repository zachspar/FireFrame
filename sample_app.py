from fastapi import FastAPI
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


class UserGetAPI(BaseReadAPIView):
    serializer_class = UserSerializer


app = FastAPI(title="Sample FireFrame App", version="0.0.0")
app.include_router(UserGetAPI.as_router())
