"""
This is a boilerplate pipeline 'union_tablas'
generated using Kedro 1.0.0
"""
import pandas as pd

def eliminar_columnas(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    return df.drop(columns=cols, errors="ignore")


def renombrar_columna(df: pd.DataFrame, viejo: str, nuevo: str) -> pd.DataFrame:
    return df.rename(columns={viejo: nuevo})


def unir_partidos_y_jugadores(details: pd.DataFrame, games: pd.DataFrame) -> pd.DataFrame:
    merged = details.merge(
        games,
        on="GAME_ID",
        how="left"
    )
    merged["TEAM_TYPE"] = merged.apply(
        lambda row: "HOME" if row["TEAM_ID"] == row["HOME_TEAM_ID"] else "AWAY",
        axis=1
    )
    return merged


def unir_con_info_equipos(df_final: pd.DataFrame, teams_info: pd.DataFrame) -> pd.DataFrame:
    df = df_final.merge(
        teams_info,
        on='TEAM_ID',
        how='left',
        suffixes=('', '_team')
    )
    return df


