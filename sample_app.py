"""A sample FireFrame API."""
from fireframe.core.api import FireFrameAPI
from fireframe.core.mixins import crud_router
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


class Item(Model):
    """
    Item model.

    Inherits from FireFrame's Model.
    """

    class Meta:
        collection_name = "items_sample_collection"

    name: str
    price: float
    is_offer: bool
    stock: int


class ItemSerializer(ModelSerializer):
    """
    Item serializer.

    Inherits from FireFrame's ModelSerializer.
    """

    class Meta:
        model = Item
        fields = ["name", "price", "is_offer", "stock"]


app = FireFrameAPI(title="Sample FireFrame App", version="0.0.0")

# routes from mixin
app.include_router(crud_router(UserSerializer), tags=["Users"], prefix="/users")
app.include_router(crud_router(ItemSerializer), tags=["Items"], prefix="/items")
