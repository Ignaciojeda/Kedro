# src/proyecto_ml/pipelines/data_engineering/pipeline.py

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    clean_games_data,
    clean_teams_data,
    handle_missing_values,
    create_team_features_base,
    create_game_level_features,
    prepare_model_inputs,
    validate_data_quality,
    create_eda_visualizations
)

def create_pipeline(**kwargs) -> Pipeline:
    """
    Crear pipeline de ingeniería de datos adaptado al catálogo existente.
    """
    return pipeline(
        [
            # Node 1: Limpieza de datos de partidos
            node(
                func=clean_games_data,
                inputs="games",                # <-- nombre simple
                outputs="games_limpios",
                name="clean_games_data_node",
                tags=["cleaning", "preprocessing"]
            ),
            
            # Node 2: Limpieza de datos de equipos
            node(
                func=clean_teams_data,
                inputs="teams",                # <-- nombre simple
                outputs="teams_clean",
                name="clean_teams_data_node",
                tags=["cleaning", "preprocessing"]
            ),
            
            # Node 3: Manejo de valores missing
            node(
                func=handle_missing_values,
                inputs="games_limpios",
                outputs="games_validated",
                name="handle_missing_values_node",
                tags=["cleaning", "missing_values"]
            ),
            
            # Node 4: Crear features base de equipos
            node(
                func=create_team_features_base,
                inputs=["games_validated", "teams_clean"],
                outputs="team_features_base",
                name="create_team_features_base_node",
                tags=["feature_engineering", "aggregation"]
            ),
            
            # Node 5: Crear features a nivel de partido
            node(
                func=create_game_level_features,
                inputs=["games_validated", "team_features_base"],
                outputs="game_level_features",
                name="create_game_level_features_node",
                tags=["feature_engineering", "model_prep"]
            ),
            
            # Node 6: Preparar inputs para modelado
            node(
                func=prepare_model_inputs,
                inputs="game_level_features",
                outputs=["model_input_classification", "model_input_regression"],
                name="prepare_model_inputs_node",
                tags=["model_prep", "final_output"]
            ),
            
            # Node 7: Validación de calidad de datos
            node(
                func=validate_data_quality,
                inputs=["games_validated", "team_features_base", "game_level_features"],
                outputs="validation_report",
                name="validate_data_quality_node",
                tags=["validation", "quality_check"]
            ),
            
            # Node 8: Crear visualizaciones EDA
            node(
                func=create_eda_visualizations,
                inputs="games_validated",
                outputs="eda_figs",
                name="create_eda_visualizations_node",
                tags=["visualization", "eda"]
            )
        ],
        tags="data_engineering"  # <-- mantenemos la etiqueta, pero SIN namespace
        # namespace="data_engineering"  # ❌ Eliminado
    )
