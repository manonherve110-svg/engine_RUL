import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler



#vu que l'usure n'est pas observable au debut du cycle 
# on va faire du clipping : Toute valeur supérieure à max_rul est remplacée par max_rul
# but ne pas demander au modele de comprendre au moment du moteur sain de voir les petites differences qui ferai dire pourquoi
# le RUL commence a diminuer.

def calculate_rul(train_df,max_rul=125):
    """
    Calcule le RUL pour chaque ligne du dataset d'entraînement.
    Applique également un clipping (Piecewise Linear RUL) si max_rul est défini.
    """

    df = train_df.copy()

    max_cycles = df.groupby("unit_id")["cycle"].max().reset_index()
    max_cycles.rename(columns={'cycle': 'max_cycle'}, inplace=True)

    df = df.merge(max_cycles, on='unit_id', how='left')

    #calcul du RUL
    df['RUL'] = df['max_cycle'] - df['cycle']
    df.drop('max_cycle', axis=1, inplace=True)

    # Clipping du RUL 
    if max_rul is not None:
        df['RUL'] = df['RUL'].clip(upper=max_rul)

    return df



# on a vu dans le notebook que  : sensor_1', 'sensor_5', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19'
# sont des capteur constant donc pas besoin de les garder.

def drop_constant_columns(train_df,test_df):
    """
    Supprime les colonnes qui ont une variance nulle (constantes) dans le train set.
    """

    constant_columns = ["sensor_1", "sensor_5", "sensor_10", "sensor_16", "sensor_18", "sensor_19"]
    train_df = train_df.drop(columns=constant_columns)
    test_df = test_df.drop(columns=constant_columns)

    return train_df, test_df


# MinMaxScaler() est une classe de scikit-learn qui sert à normaliser les données en les ramenant dans 
# un intervalle donné, généralement entre 0 et 1.

def scale_features(train_df, test_df, columns_to_scale):
    """
    Normalise les capteurs entre 0 et 1 en utilisant MinMaxScaler.
    ATTENTION : Le scaler est "fit" uniquement sur le train_df pour éviter la fuite de données (data leakage).
    """

    scaler = MinMaxScaler()

    train_scaled = train_df.copy()
    test_scaled = test_df.copy()

    # la fonction fit spermet de recuperer le min et le max
    # on utilise fit dans le train car on a toutes les valeurs et on peut donc trouver le min et le max de chaque capteur.
    # dans le test on utilise les min et max du train pour normaliser les valeurs du test.

    train_scaled[columns_to_scale] = scaler.fit_transform(train_df[columns_to_scale])
    test_scaled[columns_to_scale] = scaler.transform(test_df[columns_to_scale])

    return train_scaled, test_scaled, scaler


def get_last_cycle_test(test_df):
    """
    Pour l'évaluation finale avec RUL_XXXX.txt, on a besoin uniquement de 
    la dernière observation (dernier cycle) de chaque moteur du test set.
    """
    return test_df.groupby('unit_id').last().reset_index()






