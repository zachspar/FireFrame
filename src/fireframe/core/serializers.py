"""
FireFrame Core Serializers.
"""
import inspect

from pydantic import BaseModel as BaseSerialzer, create_model
from pydantic.fields import FieldInfo

from .models import Model


__all__ = [
    "ModelSerializer",
]


def _create_serializer_class(model_class, fields):
    class_name = f"{model_class.__name__}Serializer"
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

        fields = getattr(cls.Meta, "fields", None)

        # If fields is not specified, use all fields from the model
        if not fields:
            raise TypeError("Meta.fields must be specified and not empty")

        # Create the Pydantic serializer class
        cls._serializer_class = _create_serializer_class(cls.Meta.model, fields)

        # create each field as an annotation
        for field in fields:
            cls.__annotations__[field] = cls._serializer_class.__annotations__[field]

    @classmethod
    def from_model(cls, model: Model):
        if not isinstance(model, cls.Meta.model):
            raise TypeError(f"Model must be of type {cls.Meta.model}")

        serializer_class = cls._serializer_class

        # Convert the model instance to a dictionary
        data = {field: getattr(model, field) for field in cls.Meta.fields}

        # Create a serializer instance from the dictionary
        serializer = serializer_class(**data)

        return serializer

    @classmethod
    def to_model(cls, serializer: BaseSerialzer):
        if not isinstance(serializer, cls._serializer_class):
            raise TypeError(f"Serializer must be of type {cls._serializer_class}")

        # Create a new model instance
        model = cls.Meta.model()

        # Set the model attributes from the serializer
        for field, value in serializer.model_dump().items():
            setattr(model, field, value)

        return model
