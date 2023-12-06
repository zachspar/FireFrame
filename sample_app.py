"""A sample FireFrame API."""
from fireframe.core.api import FireFrameAPI
from fireframe.core.views import BaseListAPIView
from fireframe.core.viewsets import crud_viewset
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


class ItemListView(BaseListAPIView):
    """
    Item list view.

    Inherits from FireFrame's BaseListAPIView.
    """

    serializer_class = ItemSerializer


class UserListView(BaseListAPIView):
    """
    User list view.

    Inherits from FireFrame's BaseListAPIView.
    """

    serializer_class = UserSerializer


app = FireFrameAPI(title="Sample FireFrame App", version="0.0.0")

# include routes from viewsets and views
app.include_router(crud_viewset(UserSerializer), tags=["Users"], prefix="/users")
app.include_router(UserListView(), tags=["Users"], prefix="/users")
app.include_router(crud_viewset(ItemSerializer), tags=["Items"], prefix="/items")
app.include_router(ItemListView(), tags=["Items"], prefix="/items")
