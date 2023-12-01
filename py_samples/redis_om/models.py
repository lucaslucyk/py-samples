# models.py
from aredis_om import Field, JsonModel


class Sample(JsonModel):
    foo: str = Field(index=True, alias="f", primary_key=True)
    bar: str = Field(alias="b")

    class Meta:
        extra = "ignore"
        model_key_prefix = "Sample"
        global_key_prefix = "py_sample"
        populate_by_name = True
        allow_population_by_field_name = True
