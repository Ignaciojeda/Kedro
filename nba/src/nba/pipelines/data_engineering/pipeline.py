from kedro.pipeline import Pipeline, node, pipeline
from .nodes import (
    validate_games_schema, clean_games, aggregate_details_to_teamgame,
    make_team_form_features, build_model_inputs
)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=validate_games_schema,
            inputs=dict(games="games", required_cols="params:required_game_cols"),
            outputs="games_validated",
            name="validate_games_schema_node",
        ),
        node(
            func=clean_games,
            inputs=dict(games="games_validated", outlier_zscore="params:outlier_zscore"),
            outputs="games_clean",
            name="clean_games_node",
        ),
        node(
            func=aggregate_details_to_teamgame,
            inputs="games_details",
            outputs="details_agg_teamgame",
            name="aggregate_details_node",
        ),
        node(
            func=make_team_form_features,
            inputs=dict(
                games_clean="games_clean",
                details_agg="details_agg_teamgame",
                rolling_window="params:rolling_window",
                min_games_per_season="params:min_games_per_season",
            ),
            outputs="game_level_features",
            name="make_team_form_features_node",
        ),
        node(
            func=build_model_inputs,
            inputs="game_level_features",
            outputs=["model_input_classification","model_input_regression"],
            name="build_model_inputs_node",
        ),
    ])
