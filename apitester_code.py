###Fichier Code Apitester
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)


def load_csv(file):
    df = pd.read_csv(file)
    return df.to_dict(orient="records")  ##pour convertir au format JSON


@app.route("/csv/<filename>", methods=["GET"])
def get_csv_content(filename):
    data = load_csv(filename)
    if data is None:
        return jsonify({"error": "File not found"}), 404
    return jsonify(data)


## accès au fichier CSV

if __name__ == "__main__":
    app.run(debug=True)
##Code pour tester l'API
