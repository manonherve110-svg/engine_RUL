import pandas as pd
from pathlib import Path

columns = ["unit_id", "cycle", "setting_1", "setting_2", "setting_3"]
sensors = [f"sensor_{i}" for i in range(1, 22)]
columns += sensors

def load_train(path):
    return pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        names=columns
    )


def load_test(path):
    return pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        names=columns
    )


def load_rul(path):
    return pd.read_csv(
        path,
        header=None,
        names=["RUL"]
    )