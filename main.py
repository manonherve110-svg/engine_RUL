from src.data.loader import load_train, load_test, load_rul
from src.data.preprocessing import calculate_rul, drop_constant_columns, scale_features
from src.data.windowing import create_sequences_train, create_sequences_test
import numpy as np
from sklearn.metrics import mean_squared_error
from src.models.LSTM import build_lstm_model


# 1. Chargement
print("Chargement des données")
train_df = load_train("data/CMAPSSData/train_FD001.txt")
test_df = load_test("data/CMAPSSData/test_FD001.txt")
y_test = load_rul("data/CMAPSSData/RUL_FD001.txt")
print("fin Chargement des données")

# 2. Preprocessing
print("Preprocessing")
train_df = calculate_rul(train_df, max_rul=125)
train_df, test_df = drop_constant_columns(train_df, test_df)

features = [col for col in train_df.columns if col not in ['unit_id', 'cycle', 'RUL']]
train_df, test_df, scaler = scale_features(train_df, test_df, features)
print("fin Preprocessing")

# 3. Windowing
print("Création des séquences temporelles")
SEQ_LENGTH = 30

X_train, y_train = create_sequences_train(train_df, SEQ_LENGTH, features)
X_test = create_sequences_test(test_df, SEQ_LENGTH, features)
y_test = y_test['RUL'].values # On convertit en numpy array

# print(f"Forme de X_train : {X_train.shape} (Nb séquences, Nb cycles, Nb capteurs)")
# print(f"Forme de X_test : {X_test.shape}")


# 4. Création du modèle
print("Création du modèle LSTM...")
nb_features = X_train.shape[2]
model = build_lstm_model(SEQ_LENGTH, nb_features)
print("fin Création du modèle LSTM")

# 5. Entraînement du modèle
print("Début de l'entraînement...")
history = model.fit(
    X_train, y_train,
    epochs=20,         
    batch_size=64,      
    validation_split=0.1, 
    verbose=1
)


# 6. Évaluation sur le set de test (les vraies prédictions !)
print("Évaluation sur le Test set...")
y_pred = model.predict(X_test)
y_pred = y_pred.flatten()

for i, rul in enumerate(y_pred):
    print(f"Moteur {i+1} : RUL prédit = {rul:.2f} cycles")
    

# Calcul du RMSE (Root Mean Squared Error)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"\n>>> RMSE sur le set de test FD001 : {rmse:.2f} cycles <<<")








