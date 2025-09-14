"""
This is a boilerplate pipeline 'Preprocesamiento'
generated using Kedro 1.0.0
"""
import pandas as pd

def _is_true(x: pd.Series) -> pd.Series:
    return x == 1

def preprocces_games(games: pd.DataFrame) -> pd.DataFrame:

    games['HOME_TEAM_WINS'] = _is_true(games['HOME_TEAM_WINS'])

    return games