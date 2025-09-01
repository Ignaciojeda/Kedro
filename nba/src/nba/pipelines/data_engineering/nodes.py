import logging
import pandas as pd
import numpy as np
from typing import Tuple

logger = logging.getLogger(__name__)

def validate_games_schema(games: pd.DataFrame, required_cols: list[str]) -> pd.DataFrame:
    """
    Comprueba columnas críticas y tipos básicos.
    - No filas vacías
    - Columnas requeridas presentes
    """
    assert not games.empty, "games.csv está vacío."
    missing = set(required_cols) - set(games.columns)
    assert not missing, f"Faltan columnas en games: {missing}"
    if not np.issubdtype(games["GAME_DATE_EST"].dtype, np.datetime64):
        games["GAME_DATE_EST"] = pd.to_datetime(games["GAME_DATE_EST"], errors="coerce")
    logger.info("Games schema validado: %s filas, %s columnas", *games.shape)
    return games

def clean_games(games: pd.DataFrame, outlier_zscore: float) -> pd.DataFrame:
    """
    Limpieza básica:
    - Deduplicados por GAME_ID
    - Coherencia de puntos (no negativos)
    - Outliers de puntos por z-score truncado
    """
    games = games.drop_duplicates(subset=["GAME_ID"]).copy()
    for col in ["PTS_home", "PTS_away"]:
        games[col] = pd.to_numeric(games[col], errors="coerce")
        games.loc[games[col] < 0, col] = np.nan
    # outliers por z-score (suave)
    for col in ["PTS_home", "PTS_away"]:
        z = (games[col] - games[col].mean()) / games[col].std(ddof=0)
        games.loc[(z.abs() > outlier_zscore), col] = np.nan
    # márgen y totales
    games["MARGIN"] = games["PTS_home"] - games["PTS_away"]
    games["TOTAL_POINTS"] = games["PTS_home"] + games["PTS_away"]
    return games

def aggregate_details_to_teamgame(details: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega games_details a nivel (GAME_ID, TEAM_ID) con totales útiles.
    """
    cols = [c for c in details.columns if c not in {"PLAYER_ID","PLAYER_NAME"}]
    agg = details[cols].groupby(["GAME_ID","TEAM_ID"], dropna=False).sum(numeric_only=True).reset_index()
    # renombrar métricas clave para evitar colisiones
    rename = {
        "REB": "REB_team", "AST": "AST_team", "STL": "STL_team",
        "BLK": "BLK_team", "TOV": "TOV_team", "FG3M": "FG3M_team"
    }
    for k,v in rename.items():
        if k in agg.columns:
            agg = agg.rename(columns={k:v})
    return agg

def make_team_form_features(
    games_clean: pd.DataFrame, 
    details_agg: pd.DataFrame, 
    rolling_window: int,
    min_games_per_season: int
) -> pd.DataFrame:
    """
    Crea features por equipo previas al partido:
    - Promedios móviles (pts anotados/permitidos, rebotes, asistencias, pérdidas, 3PT)
    - Días de descanso (rest_days)
    - Racha (win_streak)
    Devuelve un DataFrame a nivel de partido con sufijos _home/_away.
    """
    # Preparar calendario por equipo
    base = games_clean[[
        "GAME_ID","SEASON","GAME_DATE_EST","HOME_TEAM_ID","VISITOR_TEAM_ID",
        "PTS_home","PTS_away","HOME_TEAM_WINS","MARGIN","TOTAL_POINTS"
    ]].copy()
    # reacomodar a formato long para calcular rolling por equipo
    home = base.rename(columns={
        "HOME_TEAM_ID": "TEAM_ID",
        "PTS_home": "PTS_for",
        "PTS_away": "PTS_against"
    })[["GAME_ID","SEASON","GAME_DATE_EST","TEAM_ID","PTS_for","PTS_against","HOME_TEAM_WINS"]]
    home["is_home"] = 1

    away = base.rename(columns={
        "VISITOR_TEAM_ID": "TEAM_ID",
        "PTS_away": "PTS_for",
        "PTS_home": "PTS_against"
    })[["GAME_ID","SEASON","GAME_DATE_EST","TEAM_ID","PTS_for","PTS_against","HOME_TEAM_WINS"]]
    away["is_home"] = 0
    long_df = pd.concat([home, away], ignore_index=True).sort_values(["TEAM_ID","GAME_DATE_EST"])

    # join con detalles agregados
    if "TEAM_ID" in details_agg.columns:
        long_df = long_df.merge(details_agg, on=["GAME_ID","TEAM_ID"], how="left")

    # rest_days
    long_df["prev_game_date"] = long_df.groupby(["TEAM_ID","SEASON"])["GAME_DATE_EST"].shift(1)
    long_df["rest_days"] = (long_df["GAME_DATE_EST"] - long_df["prev_game_date"]).dt.days
    long_df["rest_days"] = long_df["rest_days"].fillna(long_df["rest_days"].median())

    # win indicator (para racha)
    long_df["won_game"] = (long_df["is_home"] & (long_df["HOME_TEAM_WINS"]==1)) | \
                          ((1-long_df["is_home"]) & (long_df["HOME_TEAM_WINS"]==0))
    long_df["won_game"] = long_df["won_game"].astype(int)

    # rolling features por equipo/temporada
    features = []
    group = long_df.groupby(["TEAM_ID","SEASON"], group_keys=False)
    for col in ["PTS_for","PTS_against","REB_team","AST_team","TOV_team","FG3M_team"]:
        if col in long_df.columns:
            features.append(group[col].shift(1).rolling(rolling_window, min_periods=min_games_per_season).mean().rename(f"{col}_roll{rolling_window}"))
    # racha simple (últimos N)
    win_rate = group["won_game"].shift(1).rolling(rolling_window, min_periods=min_games_per_season).mean().rename(f"winrate_roll{rolling_window}")
    feat_df = pd.concat(features + [win_rate], axis=1)

    long_feat = pd.concat([long_df[["GAME_ID","TEAM_ID","is_home","rest_days"]], feat_df], axis=1)

    # Pivot a nivel de partido, separando home/away
    home_feat = long_feat[long_feat["is_home"]==1].drop(columns=["is_home"]).add_suffix("_home")
    away_feat = long_feat[long_feat["is_home"]==0].drop(columns=["is_home"]).add_suffix("_away")

    merged = base.merge(home_feat, left_on=["GAME_ID","HOME_TEAM_ID"], right_on=["GAME_ID_home","TEAM_ID_home"], how="left")
    merged = merged.merge(away_feat, left_on=["GAME_ID","VISITOR_TEAM_ID"], right_on=["GAME_ID_away","TEAM_ID_away"], how="left")

    # Limpieza de columnas auxiliares
    drop_cols = [c for c in merged.columns if c.endswith("_home") and c.startswith("TEAM_ID_")] + \
                [c for c in merged.columns if c.endswith("_away") and c.startswith("TEAM_ID_")] + \
                ["GAME_ID_home","GAME_ID_away"]
    merged = merged.drop(columns=drop_cols, errors="ignore")

    return merged

def build_model_inputs(game_level_features: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepara dos targets:
    - Clasificación: HOME_TEAM_WINS (0/1)
    - Regresión: MARGIN (float)
    Filtra columnas para evitar fuga de información.
    """
    # columnas numéricas de features (evitar PTS del partido ya jugado)
    leak_cols = {"PTS_home","PTS_away","TOTAL_POINTS","MARGIN","HOME_TEAM_WINS"}
    feature_cols = [c for c in game_level_features.columns 
                    if game_level_features[c].dtype.kind in "if" and c not in leak_cols]

    X = game_level_features[feature_cols].copy()
    y_cls = game_level_features["HOME_TEAM_WINS"].astype(int)
    y_reg = game_level_features["MARGIN"].astype(float)

    cls = pd.concat([X, y_cls.rename("TARGET_HOME_WIN")], axis=1)
    reg = pd.concat([X, y_reg.rename("TARGET_MARGIN")], axis=1)
    return cls, reg
