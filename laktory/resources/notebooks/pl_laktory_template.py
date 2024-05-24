# COMMAND ----------
dbutils.widgets.text("pipeline_name", "pl-stock-prices")

# COMMAND ----------
# MAGIC %pip install laktory

# COMMAND ----------
import importlib
import sys
import os
import pyspark.sql.functions as F

from laktory import dlt
from laktory import models
from laktory import get_logger
from laktory import settings

dlt.spark = spark
logger = get_logger(__name__)

# --------------------------------------------------------------------------- #
# Read Pipeline                                                               #
# --------------------------------------------------------------------------- #

pl_name = dbutils.widgets.get("pipeline_name")
filepath = f"/Workspace{settings.workspace_laktory_root}pipelines/{pl_name}.json"
with open(filepath, "r") as fp:
    pl = models.Pipeline.model_validate_json(fp.read())


# # Import User Defined Functions
# sys.path.append("/Workspace/pipelines/")
# udfs = []
# for udf in pl.udfs:
#     if udf.module_path:
#         sys.path.append(os.path.abspath(udf.module_path))
#     module = importlib.import_module(udf.module_name)
#     udfs += [getattr(module, udf.function_name)]

# --------------------------------------------------------------------------- #
# Execution                                                                   #
# --------------------------------------------------------------------------- #

pl.execute(spark=spark, udfs=udfs)
