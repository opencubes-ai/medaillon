from abc import abstractmethod
from typing import Union
from typing import Any
from laktory.models.resources.baseresource import BaseResource

pulumi_outputs = {}
"""Store pulumi outputs for deployed resources"""

pulumi_resources = {}
"""Store pulumi deployed resources"""


class PulumiResource(BaseResource):
    _pulumi_resources: dict[str, Any] = {}

    # ----------------------------------------------------------------------- #
    # Properties                                                              #
    # ----------------------------------------------------------------------- #

    @property
    @abstractmethod
    def pulumi_resource_type(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def pulumi_cls(self):
        raise NotImplementedError()

    @property
    def base_pulumi_excludes(self) -> list[str]:
        """List of fields from base class to exclude when dumping model to pulumi"""
        return ["resource_name"]

    @property
    def pulumi_excludes(self) -> Union[list[str], dict[str, bool]]:
        """List of fields to exclude when dumping model to pulumi"""
        return []

    @property
    def pulumi_renames(self) -> dict[str, str]:
        """Map of fields to rename when dumping model to pulumi"""
        return {}

    # ----------------------------------------------------------------------- #
    # Methods                                                                 #
    # ----------------------------------------------------------------------- #

    @property
    def pulumi_properties(self) -> dict:
        """
        Dump model and customize it to be used as an input for a pulumi
        resource:

        * dump the model
        * remove excludes defined in `self.pulumi_excludes`
        * rename keys according to `self.pulumi_renames`
        * inject variables

        Returns
        -------
        :
            Pulumi-safe model dump
        """
        excludes = self.base_pulumi_excludes
        if isinstance(self.pulumi_excludes, dict):
            excludes = {k: True for k in excludes}
            excludes.update(self.pulumi_excludes)
        else:
            excludes = self.base_pulumi_excludes + self.pulumi_excludes

        d = super().model_dump(exclude=excludes, exclude_none=True)
        for k, v in self.pulumi_renames.items():
            d[v] = d.pop(k)
        d = self.inject_vars(d)
        return d

    def deploy(self, opts=None):

        import pulumi

        class LaktoryComponent(pulumi.ComponentResource):
            pass

        provider = "databricks"  # TODO: Review
        t = f"laktory:{provider}:{type(self).__name__.replace('Pulumi', '')}"

        parent = LaktoryComponent(
            t,
            self.resource_name,
            {},
            opts=opts,
        )
        self._pulumi_resources = {
            self.resource_name: parent
        }

        opts = pulumi.ResourceOptions(
            parent=parent,
            delete_before_replace=True,
        )

        for r in self.all_resources:
            properties = r.pulumi_properties
            properties = self.resolve_vars(properties, target="pulumi_py")
            _r = r.pulumi_cls(r.resource_name, **properties, opts=opts)
            self._pulumi_resources[r.resource_name] = _r

            # TODO: Store other properties (like url, etc.).
            for k in [
                "id",
                "object_id",
            ]:
                if hasattr(_r, k):
                    pulumi_outputs[f"{r.resource_name}.{k}"] = getattr(_r, k)

        # Save resources
        for k, v in self._pulumi_resources.items():
            pulumi_resources[k] = v

        # Return resources
        return self._pulumi_resources
