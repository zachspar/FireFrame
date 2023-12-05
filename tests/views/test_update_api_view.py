"""
Test the BaseUpdateAPIView class.
"""
import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.models import Model
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseUpdateAPIView
from ._fixtures import test_thread


class TestUpdateAPIView:
    def test_view_no_serializer(self):
        """
        Test the BaseUpdateAPIView raises TypeError when
        serializer_class is not a subclass of ModelSerializer.
        """

        class TestBadView(BaseUpdateAPIView):
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

    def test_update_view_ok(self, test_thread, _TestModel):
        """
        Test the BaseUpdateAPIView works as expected.
        """

        class TestSerializer(ModelSerializer):
            class Meta:
                model = _TestModel
                fields = ["example"]

        class TestUpdateView(BaseUpdateAPIView):
            serializer_class = TestSerializer

        instance_id: str = _TestModel(example=f"This is a test from test_update_view_ok method").save().id
        app = FireFrameAPI()
        app.include_router(TestUpdateView.as_router())
        client = TestClient(app)
        response = client.put(f"/{instance_id}", json={"example": "This is a test from test_update_view_ok method"})
        assert response.status_code == 200
        assert response.json() == {"example": "This is a test from test_update_view_ok method"}
        assert _TestModel.collection.get(instance_id).example == "This is a test from test_update_view_ok method"
