import pandas as pd
import matplotlib.pyplot as plt
import io

def eda_basic_plots(game_level_features: pd.DataFrame) -> dict:
    """
    Genera figuras clave (guardadas por el MatplotlibWriter si lo declaras en el catalog).
    Retorna un dict de figuras para que kedro las serialice.
    """
    figs = {}
    # Distribución de margen
    fig1 = plt.figure()
    game_level_features["MARGIN"].dropna().hist(bins=50)
    plt.title("Distribución del margen (home - away)")
    figs["margin_hist"] = fig1

    # Winrate vs rest_days_home
    if "rest_days_home" in game_level_features.columns:
        fig2 = plt.figure()
        tmp = game_level_features.copy()
        tmp["TARGET_HOME_WIN"] = (tmp["HOME_TEAM_WINS"]==1).astype(int)
        tmp.groupby(pd.cut(tmp["rest_days_home"], bins=[0,1,2,3,7]))["TARGET_HOME_WIN"].mean().plot(kind="bar")
        plt.title("Winrate local por días de descanso (home)")
        figs["winrate_by_rest"] = fig2

    return figs
