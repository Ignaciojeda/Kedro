from __future__ import annotations
from kedro.pipeline import Pipeline
from nba.pipelines.data_engineering import pipeline as de
from nba.pipelines.union_tablas import pipeline as ut 

def register_pipelines() -> dict[str, Pipeline]:
    data_engineering = de.create_pipeline().tag("crisp_prep")
    union_tablas = ut.create_pipeline().tag("union")

    return {
        "__default__": data_engineering + union_tablas ,
        "data_engineering": data_engineering,
        "de": data_engineering,
        "union_tablas": union_tablas

    }
