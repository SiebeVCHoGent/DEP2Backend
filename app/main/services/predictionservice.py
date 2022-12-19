import random
from pathlib import Path

import pandas as pd
import pickle
from tensorflow import keras

COLUMNS = ["aantalwerknemers", "omzet", "omzetperwerknemer", "balanstotaal"]
for i in range(0, 3):
    COLUMNS.append("verstedelijkingsgraad_" + str(i))

for i in range(0, 20):
    # convert to string: 0 = A
    COLUMNS.append("hoofdsector_" + chr(i+65))


def predict(verstedelijkingsgraad: int, aantalwerknemers: int, omzet: int, omzetperwerknemer: int, balanstotaal: int, hoofdsector: str):
    normalizer_path = Path(__file__).parent.parent.parent.parent / "files" / "normalizer.h5"
    model_path = Path(__file__).parent.parent.parent.parent / 'files' / 'model.h5'

    # Get the model and normalizer
    with open(normalizer_path, 'rb') as f:
        normalizer = pickle.load(f)
    model = keras.models.load_model(model_path)

    df = clean_data(verstedelijkingsgraad, aantalwerknemers, omzet, omzetperwerknemer, balanstotaal, hoofdsector)

    df = normalizer.transform(df)
    prediction = model.predict(df)
    return float(prediction[0][0])


def clean_data(verstedelijkingsgraad: int, aantalwerknemers: int, omzet: int, omzetperwerknemer: int, balanstotaal: int, hoofdsector: str):
    hoofdsector = hoofdsector.upper()
    hoofdsectorArr = [0] * 20
    hoofdsectorArr[ord(hoofdsector) - 65] = 1

    verstedelijkingsgraadArr = [0] * 3
    verstedelijkingsgraadArr[verstedelijkingsgraad] = 1

    df = pd.DataFrame([[aantalwerknemers, omzet, omzetperwerknemer, balanstotaal, *verstedelijkingsgraadArr, *hoofdsectorArr]], columns=COLUMNS)
    return df
