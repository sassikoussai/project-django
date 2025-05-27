import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Example dataset
X = [
    [1, 2, 3],  # Features for node 1
    [4, 5, 6],  # Features for node 2
    [7, 8, 9],  # Features for node 3
    [2, 3, 4],  # Features for node 1
    [5, 6, 7],  # Features for node 2
]
y = ["node1", "node2", "node3", "node1", "node2"]  # Labels (optimal nodes)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate model accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save the trained model to a file
MODEL_PATH = "model.pkl"
with open(MODEL_PATH, "wb") as file:
    pickle.dump(model, file)

print(f"Model saved to {MODEL_PATH}")

import os
print(f"Model saved to {MODEL_PATH}, size: {os.path.getsize(MODEL_PATH)} bytes")