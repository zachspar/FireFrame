"""
Test base API view class.
"""
import pytest

from fireframe.core.models import Model
from fireframe.core.serializers import ModelSerializer
from fireframe.core.views import BaseAPIView


class TestBaseAPIView:
    def test_view_no_serializer(self):
        """
        Test the BaseAPIView raises NotImplementedError when
        _generate_routes method is not implemented.
        """

        class TestBadView(BaseAPIView):
            pass

        with pytest.raises(TypeError):
            TestBadView()

    def test_view_no_generate_routes(self):
        class TestModel(Model):
            example: str

        class TestSerializer(ModelSerializer):
            class Meta:
                model = TestModel
                fields = ["example"]

        class TestBadView(BaseAPIView):
            serializer_class = TestSerializer

        with pytest.raises(NotImplementedError):
            TestBadView()
