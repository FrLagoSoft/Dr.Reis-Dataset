# Flask micro-API for the Biscayne Bay water quality data
# Run with: python api.py   (then go to http://127.0.0.1:5000/hello)

import csv

from flask import Flask, jsonify, request

app = Flask(__name__)

# load the csv once when the server starts
# (some column names have extra spaces at the end so strip them)
with open("biscayneBay_waterquality.csv", newline="", encoding="utf-8-sig") as f:
    rows = [{k.strip(): v.strip() for k, v in r.items()} for r in csv.DictReader(f)]

# readings that get sent in with POST /data are kept here, alocated memory only
new_readings = []


@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Welcome to the Biscayne Bay Water Quality API!"}), 200


@app.route("/data", methods=["GET"])
def get_data():
    # ?limit=5 lets you choose how many rows come back (default 5)
    limit = request.args.get("limit", 5, type=int)
    if limit < 1:
        return jsonify({"error": "limit must be 1 or more"}), 400

    readings = []
    for row in rows[:limit]:
        readings.append({
            "date": row["Date m/d/y"],
            "time": row["Time hh:mm:ss"],
            "temperature_c": float(row["Temperature (c)"]),
            "salinity_ppt": float(row["Salinity (ppt)"]),
            "ph": float(row["pH"]),
            "oxygen_mg_l": float(row["ODO mg/L"]),
        })

    return jsonify({
        "total_rows": len(rows),
        "count": len(readings),
        "readings": readings,
        "added_readings": new_readings,
    }), 200 #If this all works, return a 200 response with the readings and added readings


@app.route("/data", methods=["POST"])
def add_data():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "send a JSON body"}), 400

    # temperature and ph are required, the rest is optional
    if "temperature_c" not in body or "ph" not in body:
        return jsonify({"error": "temperature_c and ph are required"}), 400 #Error handler for missing the required fields with 400

    reading = {
        "id": len(new_readings) + 1,
        "temperature_c": body["temperature_c"],
        "ph": body["ph"],
        "note": body.get("note", ""),
    }
    new_readings.append(reading)
    return jsonify({"message": "reading added", "reading": reading}), 201 #Sucess response 201 adding new reading 


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "route not found"}), 404 #Error handler for 404 errors


if __name__ == "__main__":
    app.run(debug=True)
