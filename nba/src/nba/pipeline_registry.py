from kedro.pipeline import Pipeline

from .pipelines.data_engineering import pipeline as de_pipeline
from .pipelines.union_tablas import pipeline as ut_pipeline
from .pipelines.classification import pipeline as classification_pipeline
from.pipelines.regression import pipeline as regression_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    data_engineering = de_pipeline.create_pipeline()
    union_tablas = ut_pipeline.create_pipeline()
    classification = classification_pipeline.create_pipeline()
    regression = regression_pipeline.create_pipeline()

    return {
        "__default__": data_engineering + union_tablas + classification,
        "data_engineering": data_engineering,
        "union_tablas": union_tablas,
        "classification": classification,
        "complete": data_engineering + union_tablas + classification,
        "regression": regression
    }