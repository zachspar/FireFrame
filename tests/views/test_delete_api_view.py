"""
Test the BaseDestroyAPIView class.
"""
import json

import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseDestroyAPIView
from ._fixtures import test_model_primitive_1


class TestDestroyAPIView:
    def test_view_no_serializer(self):
        """
        Test the BaseDestroyAPIView raises TypeError when
        serializer_class is not a subclass of ModelSerializer.
        """

        class TestBadView(BaseDestroyAPIView):
            pass

        with pytest.raises(TypeError):
            TestBadView()

    def test_destroy_view_ok(self, test_model_primitive_1):
        """
        Test the BaseDestroyAPIView works as expected.
        """

        class TestDestroySerializer(ModelSerializer):
            class Meta:
                model = test_model_primitive_1
                fields = ["example"]

        class TestDestroyView(BaseDestroyAPIView):
            serializer_class = TestDestroySerializer

        instance_id: str = test_model_primitive_1(example=f"This is a test from test_destroy_view_ok method").save().id
        app = FireFrameAPI()
        app.include_router(TestDestroyView())
        client = TestClient(app)

        # delete instance using API
        response = client.delete(f"/{instance_id}")
        assert response.status_code == 204
        with pytest.raises(json.decoder.JSONDecodeError):
            response.json()

        # ensure same response again
        response = client.delete(f"/{instance_id}")
        assert response.status_code == 204
        with pytest.raises(json.decoder.JSONDecodeError):
            response.json()

        # ensure instance is deleted from database
        assert test_model_primitive_1.collection.get(instance_id) is None
