import numpy as np 



def create_sequences_train(df, sequence_length, feature_columns):
    """
    Crée des séquences (fenêtres glissantes) pour l'entraînement.
    Chaque séquence contient l'historique des capteurs sur 'sequence_length' cycles.
    """
    X, y = [], []
    
    for unit_id in df['unit_id'].unique():
        unit_data = df[df['unit_id'] == unit_id]
        
        # Extraire les valeurs des capteurs et de la cible (RUL)
        features = unit_data[feature_columns].values
        rul = unit_data['RUL'].values
        
        # Création des fenêtres glissantes
        for i in range(len(unit_data) - sequence_length + 1):
            X.append(features[i : i + sequence_length])
            # La cible est le RUL au DERNIER cycle de la séquence
            y.append(rul[i + sequence_length - 1])
            
    return np.array(X), np.array(y)




def create_sequences_test(df, sequence_length, feature_columns):
    """
    Crée des séquences pour le test.
    ATTENTION : Pour le test, on ne veut que la DERNIÈRE séquence de chaque moteur,
    car c'est là qu'on doit prédire le RUL (pour comparer avec RUL_FD001.txt).
    """
    X = []
    
    for unit_id in df['unit_id'].unique():
        unit_data = df[df['unit_id'] == unit_id]
        features = unit_data[feature_columns].values
        
        # On vérifie que le moteur a assez de cycles pour former une séquence
        if len(unit_data) >= sequence_length:
            X.append(features[-sequence_length:]) # On prend les N derniers cycles
        else:
            # Si le moteur a moins de cycles que la taille de la séquence (rare mais possible),
            # on complète avec des zéros au début (padding).
            pad_length = sequence_length - len(unit_data)
            pad = np.zeros((pad_length, features.shape[1]))
            padded_features = np.vstack([pad, features])
            X.append(padded_features)
            
    return np.array(X)