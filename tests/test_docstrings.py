import re

import pytest
import pytest_examples
from pyspark.sql import SparkSession
from pytest_examples import CodeExample
from pytest_examples import EvalExample
from pytest_examples import find_examples

# Change examples print prefix to be ruff lint compatible
comment_prefix = "# > "
pytest_examples.run_code.comment_prefix = comment_prefix
pytest_examples.run_code.comment_prefix_re = re.compile(
    f"^ *{re.escape(comment_prefix)}", re.MULTILINE
)


spark = (
    SparkSession.builder.appName("Docs")
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .getOrCreate()
)
spark.conf.set("spark.sql.session.timeZone", "UTC")


# --------------------------------------------------------------------------- #
# Datetime                                                                    #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./laktory/datetime.py"), ids=str)
def test_docstrings_datetime(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_update(example)
    else:
        eval_example.lint_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_check(example)


# --------------------------------------------------------------------------- #
# Dispatcher                                                                  #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./laktory/dispatcher/"), ids=str)
def test_docstrings_dispatcher(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_update(example)
    else:
        eval_example.lint_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_check(example)


# --------------------------------------------------------------------------- #
# DLT                                                                         #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./laktory/dlt"), ids=str)
def test_docstrings_dlt(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_update(
                example,
                module_globals={
                    "spark": spark,
                    "display": lambda x: x,
                },
            )
    else:
        eval_example.lint_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_check(
                example,
                module_globals={
                    "spark": spark,
                    "display": lambda x: x,
                },
            )


# --------------------------------------------------------------------------- #
# Models                                                                      #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./laktory/models"), ids=str)
def test_docstrings_models(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_update(
                example,
                module_globals={"spark": spark},
            )
    else:
        eval_example.lint_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_check(example, module_globals={"spark": spark})


# --------------------------------------------------------------------------- #
# Polars DataFrame                                                            #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "example", find_examples("./laktory/polars/dataframe"), ids=str
)
def test_docstrings_polars_dataframe(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_update(example)
    else:
        eval_example.lint_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_check(example)


# --------------------------------------------------------------------------- #
# Polars Expressions                                                          #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "example", find_examples("./laktory/polars/expressions"), ids=str
)
def test_docstrings_polars_expressions(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_update(example)
    else:
        eval_example.lint_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_check(example)


# --------------------------------------------------------------------------- #
# Spark DataFrame                                                             #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./laktory/spark/dataframe"), ids=str)
def test_docstrings_spark_dataframe(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_update(example, module_globals={"spark": spark})
    else:
        eval_example.lint_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_check(example, module_globals={"spark": spark})


# --------------------------------------------------------------------------- #
# Spark Functions                                                             #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./laktory/spark/functions"), ids=str)
def test_docstrings_spark_functions(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_update(example, module_globals={"spark": spark})
    else:
        eval_example.lint_ruff(example)
        if "tag:skip-run" not in example.prefix_tags():
            eval_example.run_print_check(example, module_globals={"spark": spark})


# --------------------------------------------------------------------------- #
# Markdowns                                                                   #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./docs/"), ids=str)
def test_docstrings_markdowns(example: CodeExample, eval_example: EvalExample):
    """
    Examples in documentation are not designed to be run in isolation. We only format
    them. To be investigated if there is a better approach.
    """

    if eval_example.update_examples:
        eval_example.format_ruff(example)
    else:
        eval_example.lint_ruff(example)
