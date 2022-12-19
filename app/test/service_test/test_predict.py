from app.main.services.predictionservice import predict


def test_predict():
    prediction_data = {
        "verstedelijkingsgraad": 2,
        "aantalwerknemers": 27,
        "omzet": 5439,
        "balanstotaal": 78782159,
        "omzetperwerknemer": 5439999 / 27,
        "hoofdsector": "O"
    }
    prediction = predict(**prediction_data)
    print(prediction)
