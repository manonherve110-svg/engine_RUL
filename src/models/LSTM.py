from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def build_lstm_model(sequence_length, nb_features):
    """
    Construit un modèle LSTM pour la prédiction du RUL.
    """
    model = Sequential()

    #premiere couche : lit les équeces temporelles
    model.add(LSTM(units=64, return_sequences=True, input_shape=(sequence_length, nb_features)))
    model.add(Dropout(0.2))

    #dexieme couche 
    model.add(LSTM(units=32, return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(units=16, activation='relu'))


    model.add(Dense(1))  # Prédiction d'une seule valeur (RUL)
    
    model.compile(optimizer='adam', loss='mse')
    
    return model