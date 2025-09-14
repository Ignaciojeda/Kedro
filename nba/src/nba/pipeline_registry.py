from __future__ import annotations
from kedro.pipeline import Pipeline
from nba.pipelines.Preprocesamiento import pipeline as pre
from nba.pipelines.data_engineering import pipeline as de
from nba.pipelines.reporting import pipeline as rep
from nba.pipelines.modeling import pipeline as modeling  # <-- nuevo import

def register_pipelines() -> dict[str, Pipeline]:
    data_engineering = de.create_pipeline().tag("crisp_prep")
    reporting = rep.create_pipeline().tag("crisp_eda")
    model_pipeline = modeling.create_pipeline().tag("modeling")  # <-- pipeline de modelado
    Preprocesamiento = pre.create_pipeline().tag("Proce")

    return {
        "__default__": data_engineering + reporting + model_pipeline + Preprocesamiento,
        "de": data_engineering,
        "rep": reporting,
        "modeling": model_pipeline,  # <-- registrar pipeline
        "pre": Preprocesamiento

    }
