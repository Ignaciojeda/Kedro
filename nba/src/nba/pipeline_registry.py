from __future__ import annotations
from kedro.pipeline import Pipeline
from nba.pipelines.data_engineering import pipeline as de
from nba.pipelines.reporting import pipeline as rep
from nba.pipelines.modeling import pipeline as modeling  # <-- nuevo import

def register_pipelines() -> dict[str, Pipeline]:
    data_engineering = de.create_pipeline().tag("crisp_prep")
    reporting = rep.create_pipeline().tag("crisp_eda")
    model_pipeline = modeling.create_pipeline().tag("modeling")  # <-- pipeline de modelado

    return {
        "__default__": data_engineering + reporting + model_pipeline,
        "de": data_engineering,
        "rep": reporting,
        "modeling": model_pipeline,  # <-- registrar pipeline
    }
