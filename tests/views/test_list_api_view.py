"""
Test the BaseListAPIView class.
"""

import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseListAPIView
from ._fixtures import test_model_primitive_1, test_thread


class TestListAPIView:
    def test_view_no_serializer(self):
        """
        Test the BaseListAPIView raises TypeError when
        serializer_class is not a subclass of ModelSerializer.
        """

        class TestBadView(BaseListAPIView):
            pass

        with pytest.raises(TypeError):
            TestBadView()

    def test_list_view_ok(self, test_thread: str, test_model_primitive_1):
        """
        Test the BaseListAPIView works as expected.
        """

        class TestListSerializer(ModelSerializer):
            class Meta:
                model = test_model_primitive_1
                fields = ["example"]

        class TestListView(BaseListAPIView):
            serializer_class = TestListSerializer

        test_model_primitive_1(example=f"This is a test from test_list_view_ok method").save()
        app = FireFrameAPI()
        app.include_router(TestListView())
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == [{"example": "This is a test from test_list_view_ok method"}]

        for i in range(10):
            test_model_primitive_1(example=f"This is a test from test_list_view_ok method").save()
        response = client.get("/")
        assert response.status_code == 200
        correct_list = [{"example": "This is a test from test_list_view_ok method"} for _ in range(11)]
        assert response.json() == correct_list
