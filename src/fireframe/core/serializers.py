"""
FireFrame Core Serializers.
"""
import inspect
import sys
from uuid import uuid4

from pydantic import BaseModel as BaseSerialzer, create_model
from pydantic.fields import FieldInfo
from .models import Model

__all__ = [
    "ModelSerializer",
]


def _create_serializer_class(model_class, fields):
    class_name = f"{model_class.__name__}Serializer_{str(uuid4())[0:8]}"
    class_attrs = {
        attribute_name: (
            model_class.__annotations__.get(attribute_name),
            FieldInfo(
                title=attribute_name,
                default=None,
                alias=attribute_name,
                annotation=model_class.__annotations__.get(attribute_name),
            ),
        )
        for attribute_name, _ in inspect.getmembers(model_class)
        if attribute_name in model_class.__annotations__ and attribute_name in fields
    }
    return create_model(class_name, **class_attrs)


class ModelSerializer(BaseSerialzer):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "Meta"):
            raise TypeError("Metaclass must be defined")

        if not issubclass(cls.Meta.model, Model):
            raise TypeError("Meta.model must be a subclass of fireframe.Model")

        # NOTE: Hack to remove type annotations from the serializer class
        if sys.version_info.major == 3 and sys.version_info.minor in [8, 9]:
            for annotation in list(cls.__annotations__.keys()):
                cls.__annotations__.pop(annotation)

        fields = getattr(cls.Meta, "fields", None)

        # If fields is not specified, use all fields from the model
        if not fields:
            raise TypeError("Meta.fields must be specified and not empty")

        # create each field as an annotation
        for field in fields:
            if field not in cls.Meta.model.__annotations__:
                raise TypeError(f"Field {field} not found in model {cls.Meta.model.__name__}")
            cls.__annotations__[field] = cls.Meta.model.__annotations__[field]

    def to_model(self):
        if not issubclass(type(self), ModelSerializer):
            raise TypeError(f"Serializer must be a subclass of ModelSerializer")

        # Create a new model instance
        model = self.Meta.model()

        # Set the model attributes from the serializer
        for field, value in self.model_dump().items():
            setattr(model, field, value)

        return model
