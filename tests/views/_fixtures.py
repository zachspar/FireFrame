from uuid import uuid4

import pytest
from fireframe.core.models import Model

__all__ = [
    "test_thread",
    "test_model_primitive_1",
]


@pytest.fixture(autouse=True)
def test_thread() -> str:
    """
    Generate a unique thread id for each test.
    """
    test_thread = uuid4()
    yield str(test_thread)


@pytest.fixture(autouse=True)
def test_model_primitive_1(test_thread: str):
    """
    Test model with single string field.
    """

    class TestModelPrimitive1(Model):
        example: str

        class Meta:
            collection_name = f"test_collection_example_{test_thread[0:8]}"

    yield TestModelPrimitive1

    # cleanup test collection
    TestModelPrimitive1.collection.delete_every(child=True)


@pytest.fixture(autouse=True)
def test_model_primitive_2(test_thread: str):
    """
    Test model with four fields: str, bool, int, float
    """

    class TestModelPrimitive2(Model):
        example: str
        flag: bool
        quantity: int
        price: float

        class Meta:
            collection_name = f"test_collection_example_{test_thread[0:8]}"

    yield TestModelPrimitive2

    # cleanup test collection
    TestModelPrimitive2.collection.delete_every(child=True)
