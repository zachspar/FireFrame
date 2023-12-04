"""
Test the BaseListAPIView class.
"""

import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.models import Model
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseListAPIView
from ._fixtures import test_thread


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

    def test_list_view_ok(self, test_thread):
        """
        Test the BaseListAPIView works as expected.
        """

        class TestModel(Model):
            example: str

            class Meta:
                collection_name = f"test_collection_example_{test_thread}"

        class TestSerializer(ModelSerializer):
            class Meta:
                model = TestModel
                fields = ["example"]

        class TestListView(BaseListAPIView):
            serializer_class = TestSerializer

        TestModel(example=f"This is a test from test_list_view_ok method").save()
        app = FireFrameAPI()
        app.include_router(TestListView.as_router())
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == [{"example": "This is a test from test_list_view_ok method"}]

        for i in range(10):
            TestModel(example=f"This is a test from test_list_view_ok method").save()
        response = client.get("/")
        assert response.status_code == 200
        correct_list = [{"example": "This is a test from test_list_view_ok method"} for _ in range(11)]
        assert response.json() == correct_list

        # cleanup test collection
        TestModel.collection.delete_every(child=True)
