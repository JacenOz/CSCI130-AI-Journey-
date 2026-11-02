import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
import warnings
warnings.filterwarnings('ignore')

# Bonus Keras imports
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import set_random_seed

# Part 2: Train the classifier
def main():
    df = pd.read_csv('data/emails.csv')
    X = df.drop(columns=['label', 'base_id'])
    y = df['label']
    base_ids = df['base_id']
    
    # Train/Test Split
    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        X, y, base_ids, test_size=0.25, random_state=42
    )
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("--- PART 2: TRAINING RESULTS ---")
    print(f"Accuracy: {accuracy:.4f}\n")
    
    # Part 3: Evaluate and interrogate
    print("--- PART 3: EVALUATION ---")
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)
    print(f"True Negatives (Legit passed): {cm[0][0]}")
    print(f"False Positives (Legit flagged spam): {cm[0][1]}")
    print(f"False Negatives (Spam missed): {cm[1][0]}")
    print(f"True Positives (Spam caught): {cm[1][1]}\n")
    
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}\n")
    
    print("Feature Importances:")
    for name, importance in zip(X.columns, model.feature_importances_):
        print(f"- {name}: {importance:.4f}")
        
    print("\n--- PART 3.5: ADVERSARIAL ATTACKS ---")
    from prepare_data import extract_features
    attacks = [
        ("Hey Alice, please review the document here: http://docs.com", "Legit looking spam"),
        ("URGENT: I need the MONEY for the event immediately!!! BOB", "Spam looking legit"),
        ("Click here for a limited time offer to save cash!", "Standard spam")
    ]
    
    for text, desc in attacks:
        features = [extract_features(text)]
        pred = model.predict(features)[0]
        result = "SPAM" if pred == 1 else "LEGIT"
        print(f"Attack ({desc}): Classified as {result}")

    print("\n--- PART 3.6: DATA LEAKAGE CHECK ---")
    shared_bases = set(id_train).intersection(set(id_test))
    print(f"Base emails shared between Train and Test sets: {len(shared_bases)}/16")
    if len(shared_bases) > 0:
        print("WARNING: Data leakage detected. Variations of the same email exist in both sets.")

    print("\n--- BONUS: KERAS NEURAL NETWORK ---")
    set_random_seed(42)
    nn = Sequential([
        Dense(8, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(4, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    nn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    nn.fit(X_train, y_train, epochs=30, batch_size=8, verbose=0)
    
    _, nn_acc = nn.evaluate(X_test, y_test, verbose=0)
    print(f"Keras NN Accuracy: {nn_acc:.4f}")
    print(f"Random Forest Accuracy: {accuracy:.4f}")
    print("Comparison: The simpler Random Forest typically performs identically or better on a dataset this small and tabular.")

if __name__ == "__main__":
    main()