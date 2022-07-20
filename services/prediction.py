import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
# from tensorflow import keras
# import tensorflow as tf
import pandas as pd

frame_size = 100
hop_size = 1


# def predict(model, data):
#     data_formatted = []
#     for key in data:
#         data_formatted.append(data[key])
#     x = pd.DataFrame(data_formatted)
#     predictions = []
#     ml_model = tf.keras.models.load_model(model)
#     scaler = StandardScaler()
#     # print(x)
#     x_new = scaler.fit_transform(x)
#     s_x = pd.DataFrame(data=x_new)
#     x_frames = get_frames(s_x, frame_size, hop_size)
#     temp_data = ml_model.predict(x_frames)
#     y_pred = np.argmax(temp_data, axis=1)
#     for x in y_pred:
#         predictions.append(x)
#     return predictions


def get_frames(df, frame_size, hop_size):
    N_FEATURES = 18
    frames = []
    for i in range(0, len(df) - frame_size, hop_size):
        for j in df:
            frames.append(df[j].values[i: i + frame_size])
    frames = np.asarray(frames).reshape(-1, frame_size, N_FEATURES,1)
    return frames
