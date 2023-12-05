from uuid import uuid4

import pytest

__all__ = [
    "test_thread",
    "test_model_cleanup",
]


@pytest.fixture(autouse=True)
def test_thread() -> str:
    """
    Generate a unique thread id for each test.
    """
    test_thread = uuid4()
    yield str(test_thread)


@pytest.fixture(scope="module")
def test_model_cleanup():
    """
    Cleanup test collections after each test.
    """
