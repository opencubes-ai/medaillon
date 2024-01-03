from laktory.models.basemodel import BaseModel
from laktory.models.databricks.permission import Permission
from laktory.models.resources.pulumiresource import PulumiResource


class Permissions(BaseModel, PulumiResource):
    access_controls: list[Permission]
    pipeline_id: str = None
    job_id: str = None
    cluster_id: str = None
    directory_id: str = None
    directory_path: str = None
    experiment_id: str = None
    notebook_id: str = None
    object_type: str = None
    registered_model_id: str = None
    repo_id: str = None
    repo_path: str = None
    serving_endpoint_id: str = None
    sql_alert_id: str = None
    sql_dashboard_id: str = None
    sql_endpoint_id: str = None
    sql_query_id: str = None
    workspace_file_id: str = None
    workspace_file_path: str = None

    # ----------------------------------------------------------------------- #
    # Pulumi Methods                                                          #
    # ----------------------------------------------------------------------- #

    @property
    def pulumi_resource_type(self) -> str:
        return "databricks:Permissions"

    @property
    def pulumi_cls(self):
        import pulumi_databricks as databricks
        return databricks.Permissions