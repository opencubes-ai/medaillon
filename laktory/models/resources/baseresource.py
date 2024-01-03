import re
from pydantic import computed_field
from pydantic import Field
from pydantic import BaseModel as _BaseModel


class BaseResource(_BaseModel):
    """
    Parent class for all Laktory models deployable as one or multiple cloud
    resources. This `BaseResource` class is derived from `pydantic.BaseModel`.
    """
    resource_name_: str = Field(None, alias="resource_name", exclude=True)

    @computed_field
    def resource_name(self) -> str:
        if self.resource_name_:
            return self.resource_name_
        return self.default_resource_name

    # ----------------------------------------------------------------------- #
    # Properties                                                              #
    # ----------------------------------------------------------------------- #

    @property
    def resource_type_id(self) -> str:
        """Resource type id used to build resource name"""
        _id = type(self).__name__
        _id = re.sub(
            r"(?<!^)(?=[A-Z])", "-", _id
        ).lower()  # Convert CamelCase to kebab-case
        return _id

    @property
    def resource_key(self) -> str:
        """Resource key used to build resource name"""
        return self.name

    @property
    def default_resource_name(self) -> str:
        """Resource name `{self.resource_type}.{self.resource_key}`"""

        if self.resource_type_id not in self.resource_key:
            name = f"{self.resource_type_id}-{self.resource_key}"
        else:
            name = f"{self.resource_key}"

        return name

    @property
    def all_resources(self):
        return [
            self
        ]
