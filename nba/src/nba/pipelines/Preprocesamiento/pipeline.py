"""
This is a boilerplate pipeline 'Preprocesamiento'
generated using Kedro 1.0.0
"""

from kedro.pipeline import Node, Pipeline  # noqa
from .nodes import preprocces_games


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(
                func=preprocces_games,
                inputs="games",
                outputs="games_limpios",
                name="preprocces_games_node",
            ),






        ])
