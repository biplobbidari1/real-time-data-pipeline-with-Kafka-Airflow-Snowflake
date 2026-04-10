
import torch
import torch.nn as nn
import numpy as np
import tensorflow as tf

# PyTorch model
class RiskModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(6,128),
            nn.ReLU(),
            nn.Linear(128,64),
            nn.ReLU(),
            nn.Linear(64,1)
        )

    def forward(self,x):
        return self.net(x)

torch_model = RiskModel()

# TensorFlow model
tf_model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

def predict(features):
    arr = np.array(features, dtype=float)

    torch_pred = torch_model(torch.tensor(arr, dtype=torch.float32)).detach().numpy()
    tf_pred = tf_model(np.expand_dims(arr, axis=0)).numpy()

    return {
        "torch": float(torch_pred[0]),
        "tensorflow": float(tf_pred[0][0]),
        "ensemble": float((torch_pred[0] + tf_pred[0][0]) / 2)
    }
