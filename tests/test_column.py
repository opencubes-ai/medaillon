from medaillon.models import Column

AIRSPEED = {
    "name": "airspeed",
    "type": "double",
    "unit": "kt",
    "parent_id": "lakehouse.flights.f092",
}


def test_model():
    c0 = Column(**AIRSPEED)
    c1 = Column.model_validate(AIRSPEED)
    assert c1.type == "double"
    assert c1.catalog_name == "lakehouse"
    assert c1.schema_name == "flights"
    assert c1.table_name == "f092"
    assert "func_name" in c1.model_fields
    assert "table_name" in c1.model_computed_fields
    assert c0 == c1


def test_read():
    c0 = Column(**AIRSPEED)

    with open("./airspeed.yaml", "r") as fp:
        c1 = Column.model_validate_yaml(fp)

    with open("./airspeed.json", "r") as fp:
        c2 = Column.model_validate_json_file(fp)

    assert c1 == c0
    assert c2 == c0


if __name__ == "__main__":
    test_model()
    test_read()
