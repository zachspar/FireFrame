from fireo.typedmodels import TypedModel


__all__ = [
    "Model",
]


class Model(TypedModel):
    """
    Base model for all FireFrame models.

    Inherits from FireO's TypedModel.
    """

    class Meta:
        abstract = True
