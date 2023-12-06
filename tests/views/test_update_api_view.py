"""
Test the BaseUpdateAPIView class.
"""
import pytest
from fastapi.testclient import TestClient
from fireframe.core.api import FireFrameAPI
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseUpdateAPIView
from ._fixtures import test_model_primitive_1, test_thread


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

    def test_update_view_ok(self, test_model_primitive_1):
        """
        Test the BaseUpdateAPIView works as expected.
        """

        class TestUpdateSerializer(ModelSerializer):
            class Meta:
                model = test_model_primitive_1
                fields = ["example"]

        class TestUpdateView(BaseUpdateAPIView):
            serializer_class = TestUpdateSerializer

        instance_id: str = test_model_primitive_1(example=f"This is a test from test_update_view_ok method").save().id
        app = FireFrameAPI()
        app.include_router(TestUpdateView())
        client = TestClient(app)
        response = client.put(f"/{instance_id}", json={"example": "This is a test from test_update_view_ok method"})
        assert response.status_code == 200
        assert response.json() == {"example": "This is a test from test_update_view_ok method"}
        assert (
            test_model_primitive_1.collection.get(instance_id).example
            == "This is a test from test_update_view_ok method"
        )
