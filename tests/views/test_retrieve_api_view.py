"""
Test the BaseRetrieveAPIView class.
"""

import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseRetrieveAPIView
from ._fixtures import test_model_primitive_1


class TestRetrieveAPIView:
    def test_view_no_serializer(self):
        """
        Test the BaseRetrieveAPIView raises TypeError when
        serializer_class is not a subclass of ModelSerializer.
        """

        class TestBadView(BaseRetrieveAPIView):
            pass

        with pytest.raises(TypeError):
            TestBadView()

    def test_retrieve_view_ok(self, test_model_primitive_1):
        """
        Test the BaseRetrieveAPIView works as expected.
        """

        class TestRetrieveSerializer(ModelSerializer):
            class Meta:
                model = test_model_primitive_1
                fields = ["example"]

        class TestRetrieveView(BaseRetrieveAPIView):
            serializer_class = TestRetrieveSerializer

        instance_id: str = test_model_primitive_1(example="This is a test").save().id
        app = FireFrameAPI()
        app.include_router(TestRetrieveView())
        client = TestClient(app)
        response = client.get(f"/{instance_id}")
        assert response.status_code == 200
        assert response.json() == {"example": "This is a test"}
