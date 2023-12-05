"""
Test the BaseDestroyAPIView class.
"""
import json

import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.models import Model
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseDestroyAPIView
from ._fixtures import test_thread


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

    @pytest.fixture(scope="function")
    def _TestModel(self, test_thread) -> Model:
        """
        Cleanup the test collection after the test is done.
        """

        class TestModel(Model):
            example: str

            class Meta:
                collection_name = f"test_collection_example_{test_thread}"

        yield TestModel

        # cleanup test collection
        TestModel.collection.delete_every(child=True)

    def test_destroy_view_ok(self, test_thread: str, _TestModel: Model):
        """
        Test the BaseDestroyAPIView works as expected.
        """

        class TestSerializer(ModelSerializer):
            class Meta:
                model = _TestModel
                fields = ["example"]

        class TestDestroyView(BaseDestroyAPIView):
            serializer_class = TestSerializer

        instance_id: str = _TestModel(example=f"This is a test from test_destroy_view_ok method").save().id
        app = FireFrameAPI()
        app.include_router(TestDestroyView.as_router())
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
        assert _TestModel.collection.get(instance_id) is None
