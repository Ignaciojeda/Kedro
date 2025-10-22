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

# En union_tablas/pipeline.py
def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=eliminar_columnas,
                inputs=dict(df="data_engineering.games_validated",
                            cols="params:union_tablas.cols_games_to_drop"),
                outputs="union_tablas.games_preprocessed",  # ← NOMBRE ÚNICO
                name="eliminar_columnas_games_node",
            ),
            node(
                func=renombrar_columna,
                inputs=dict(
                    df="union_tablas.games_preprocessed",  # ← ACTUALIZADO
                    viejo="params:union_tablas.rename_columns.away_from",
                    nuevo="params:union_tablas.rename_columns.visitor_to_away"
                    ),
                outputs="union_tablas.games_renamed",  # ← NOMBRE ÚNICO
                name="renombrar_games_node",
            ),
            node(
                func=unir_partidos_y_jugadores,
                inputs=dict(details="data_engineering.games_details", 
                           games="union_tablas.games_renamed"),  # ← ACTUALIZADO
                outputs="union_tablas.games_details_merged",  # ← NOMBRE ÚNICO
                name="unir_detalles_node",
            ),
            node(
                func=eliminar_columnas,
                inputs=dict(df="data_engineering.teams", 
                           cols="params:union_tablas.cols_teams_to_drop"),
                outputs="union_tablas.teams_cleaned",  # ← NOMBRE ÚNICO
                name="eliminar_columnas_teams_node",
            ),
            node(
                func=unir_con_info_equipos,
                inputs=dict(df_final="union_tablas.games_details_merged",  # ← ACTUALIZADO
                           teams_info="union_tablas.teams_cleaned"),  # ← ACTUALIZADO
                outputs="union_tablas.final_with_teams",  # ← NOMBRE ÚNICO
                name="unir_equipos_node",
            ),
            node(
                func=eliminar_columnas,
                inputs=dict(df="union_tablas.final_with_teams",  # ← ACTUALIZADO
                            cols="params:union_tablas.cols_final_to_drop"),
                outputs="data_engineering.games_teams_details",  # ← Este puede mantenerse igual
                name="eliminar_columnas_final_node",
            )
        ],
        tags="union_tablas"  # ← Cambia el tag también
    )