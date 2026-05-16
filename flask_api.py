from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Migration Tool API is running", "status": "ok"})

@app.route("/report")
def get_report():
    with open("migration_report.json", "r", encoding="utf-8") as f:
        report = json.load(f)
    return jsonify(report)

@app.route("/data")
def get_data():
    with open("output.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify({"total": len(data), "books": data})

if __name__ == "__main__":
    app.run(debug=True, port=5000)