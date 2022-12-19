from app.main.services.predictionservice import predict


def test_predict():
    prediction_data = {
        "verstedelijkingsgraad": 1,
        "aantalwerknemers": 30,
        "omzet": 2086301253,
        "balanstotaal": 123,
        "omzetperwerknemer": 4,
        "hoofdsector": "T"
    }
    prediction = predict(**prediction_data)
    print(prediction)
