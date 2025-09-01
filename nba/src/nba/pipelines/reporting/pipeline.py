from kedro.pipeline import Pipeline, node, pipeline
from .nodes import eda_basic_plots

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=eda_basic_plots,
            inputs="game_level_features",
            outputs="eda_figs",   # usa MatplotlibWriter en catalog
            name="eda_basic_plots_node",
        )
    ])
