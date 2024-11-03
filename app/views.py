from app import app
from app import database as db

from flask import jsonify, request
from datetime import datetime

@app.get("/healthcheck")
def healthcheck():
    response = {
        "message": "Healthcheck is running",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 200
