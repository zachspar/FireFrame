"""
Test the BaseRetrieveAPIView class.
"""

import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.models import Model
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseRetrieveAPIView
from ._fixtures import test_thread


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

    def test_retrieve_view_ok(self, test_thread, _TestModel):
        """
        Test the BaseRetrieveAPIView works as expected.
        """

        class TestSerializer(ModelSerializer):
            class Meta:
                model = _TestModel
                fields = ["example"]

        class TestRetrieveView(BaseRetrieveAPIView):
            serializer_class = TestSerializer

        instance_id: str = _TestModel(example="This is a test").save().id
        app = FireFrameAPI()
        app.include_router(TestRetrieveView.as_router())
        client = TestClient(app)
        response = client.get(f"/{instance_id}")
        assert response.status_code == 200
        assert response.json() == {"example": "This is a test"}
