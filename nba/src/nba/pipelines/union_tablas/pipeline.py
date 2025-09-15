"""
This is a boilerplate pipeline 'union_tablas'
generated using Kedro 1.0.0
"""
# src/proyecto_ml/pipelines/data_engineering/pipeline.py
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    eliminar_columnas,
    renombrar_columna,
    unir_partidos_y_jugadores,
    unir_con_info_equipos
)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=eliminar_columnas,
                inputs=dict(df="data_engineering.games_validated",
                            cols="params:union_tablas.cols_games_to_drop"),
                outputs="data_engineering.games_limpios",
                name="eliminar_columnas_games_node",
            ),
            node(
                func=renombrar_columna,
                inputs=dict(
                    df="data_engineering.games_limpios",
                    viejo="params:union_tablas.rename_columns.away_from",  # esto es un string normal
                    nuevo="params:union_tablas.rename_columns.visitor_to_away"
                    ),
                outputs="data_engineering.games_preparado",
                name="renombrar_games_node",
            ),
            node(
                func=unir_partidos_y_jugadores,
                inputs=dict(details="data_engineering.games_details", games="data_engineering.games_preparado"),
                outputs="data_engineering.df_final",
                name="unir_detalles_node",
            ),
            node(
                func=eliminar_columnas,
                inputs=dict(df="data_engineering.teams", cols="params:union_tablas.cols_teams_to_drop"),
                outputs="data_engineering.teams_limpio",
                name="eliminar_columnas_teams_node",
            ),
            node(
                func=unir_con_info_equipos,
                inputs=dict(df_final="data_engineering.df_final", teams_info="data_engineering.teams_limpio"),
                outputs="data_engineering.df_final_con_equipos",
                name="unir_equipos_node",
            ),
            node(
                func=eliminar_columnas,
                inputs=dict(df="data_engineering.df_final_con_equipos",
                            cols="params:union_tablas.cols_final_to_drop"),
                outputs="data_engineering.games_teams_details",
                name="eliminar_columnas_final_node",
            )
        ],
        tags="data_engineering"
    )

