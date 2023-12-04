"""A sample FireFrame API."""
from fireframe.core.api import FireFrameAPI
from fireframe.core.mixins import CrudMixin
from fireframe.core.models import Model
from fireframe.core.serializers import ModelSerializer


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


class UserCrudAPI(CrudMixin):
    serializer_class = UserSerializer


app = FireFrameAPI(title="Sample FireFrame App", version="0.0.0")

# routes from mixin
app.include_router(UserCrudAPI.as_router(), tags=["Users"])
