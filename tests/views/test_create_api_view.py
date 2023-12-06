"""
Tests for the CreateAPIView class.
"""

import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseCreateAPIView
from ._fixtures import test_model_primitive_2, test_thread


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

    def test_create_view_ok(self, test_model_primitive_2):
        """
        Test the BaseCreateAPIView works as expected.
        """

        class TestCreateSerializer(ModelSerializer):
            class Meta:
                model = test_model_primitive_2
                fields = ["example", "flag", "price", "quantity"]

        class TestCreateView(BaseCreateAPIView):
            serializer_class = TestCreateSerializer

        app = FireFrameAPI()
        app.include_router(TestCreateView())
        client = TestClient(app)
        response = client.post(
            "/",
            json={
                "example": "This is a test from test_create_view_ok method",
                "flag": True,
                "price": 10.0,
                "quantity": 1,
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "example": "This is a test from test_create_view_ok method",
            "flag": True,
            "price": 10.0,
            "quantity": 1,
        }
