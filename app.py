# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime
import json
from resident_manager import ResidentManager
from datetime import datetime

app = Flask(__name__)
manager = ResidentManager("resident.json")

# Load vehicles
with open('resident.json') as f:
    resident_data = json.load(f)
vehicles = [v["VehicleNumber"] for v in resident_data]

# Load events from event.txt
all_events = []
with open('event.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    parts = line.strip().split(":")
    
    if parts[0] == "VEHICLE_ENTRY":
        all_events.append({
            "vehicle": parts[1],
            "event_type": "ENTRY",
            "timestamp": parts[2]
        })
    elif parts[0] == "VEHICLE_EXIT":
        all_events.append({
            "vehicle": parts[1],
            "event_type": "EXIT",
            "timestamp": parts[2]
        })
    elif parts[0] == "TRAFFIC_VIOLATION":
        all_events.append({
            "vehicle": parts[1],
            "event_type": parts[2],  # Example: SPEEDING, WRONG_WAY
            "timestamp": parts[4]
        })
    elif parts[0] == "PARKING_VIOLATION":
        all_events.append({
            "vehicle": parts[1],
            "event_type": parts[2],  # Example: NO_PARKING_ZONE
            "timestamp": parts[4]
        })
    elif parts[0] == "AFTER_HOURS_ENTRY":
        all_events.append({
            "vehicle": parts[1],
            "event_type": "AFTER_HOURS_ENTRY",
            "timestamp": parts[2]
        })
    elif parts[0] == "UNAUTHORIZED_ACCESS":
        all_events.append({
            "vehicle": parts[1],
            "event_type": "UNAUTHORIZED_ACCESS",
            "timestamp": parts[3]
        })
    else:
        # Special case: Timeout (long stay) event
        all_events.append({
            "vehicle": parts[0],
            "event_type": "TIMEOUT",
            "timestamp": parts[1]
        })

event_log = []
stats = {
    "entries": 0,
    "exits": 0,
    "violations": 0
}
current_event_index = 0

@app.route("/")
def events():
    return render_template("events.html", events=event_log,now=datetime.now())

@app.route("/generate_event")
def generate_event():
    global current_event_index

    if current_event_index < len(all_events):
        event = all_events[current_event_index]
        event_log.insert(0, event)
        if len(event_log) > 30:
            event_log.pop()

        # Update statistics
        if "ENTRY" in event["event_type"] and event["event_type"] != "AFTER_HOURS_ENTRY":
            stats["entries"] += 1
        elif "EXIT" in event["event_type"]:
            stats["exits"] += 1
        else:
            stats["violations"] += 1

        current_event_index += 1

    return jsonify({"status": "ok"})

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/residents")
def residents():
    return render_template("residents.html", residents=manager.get_all_residents())

@app.route("/add_resident", methods=["POST"])
def add_resident():
    data = request.form
    if manager.add_resident(
        data["VehicleNumber"],
        data["OwnerName"],
        data["OwnerPhone"],
        data["OwnerCampusID"],
        data["OwnerEmail"]
    ):
        manager.save_residents()
    return redirect(url_for("residents"))

@app.route("/delete_resident/<vehicle_number>")
def delete_resident(vehicle_number):
    if manager.delete_resident(vehicle_number):
        manager.save_residents()
    return redirect(url_for("residents"))

@app.route("/violations")
def violations():
    with open("violation_log.txt", "r") as f:
        violations = f.read()
    return render_template("violations.html", violations=violations)

@app.route("/reports")
def reports():
    with open("report.txt", "r") as f:
        report = f.read()
    return render_template("reports.html", report=report)

@app.route("/stats")
def get_stats():
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)





