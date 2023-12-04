"""
Tests for the CreateAPIView class.
"""

import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.models import Model
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseCreateAPIView
from ._fixtures import test_thread


class TestCreateAPIView:
    def test_view_no_serializer(self):
        """
        Test the BaseCreateAPIView raises TypeError when
        serializer_class is not a subclass of ModelSerializer.
        """

        class TestBadView(BaseCreateAPIView):
            pass

        with pytest.raises(TypeError):
            TestBadView()

    def test_create_view_ok(self, test_thread):
        """
        Test the BaseCreateAPIView works as expected.
        """

        class TestModel(Model):
            example: str
            flag: bool
            price: float

            class Meta:
                collection_name = f"test_collection_example_{test_thread}"

        class TestSerializer(ModelSerializer):
            class Meta:
                model = TestModel
                fields = ["example", "flag", "price"]

        class TestCreateView(BaseCreateAPIView):
            serializer_class = TestSerializer

        app = FireFrameAPI()
        app.include_router(TestCreateView.as_router())
        client = TestClient(app)
        response = client.post(
            "/", json={"example": "This is a test from test_create_view_ok method", "flag": True, "price": 10.0}
        )
        assert response.status_code == 201
        assert response.json() == {
            "example": "This is a test from test_create_view_ok method",
            "flag": True,
            "price": 10.0,
        }

        # cleanup test collection
        TestModel.collection.delete_every(child=True)
