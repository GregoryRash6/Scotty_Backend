import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify, render_template, redirect, request
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

password = os.getenv("password")
url = os.getenv("url")
port = os.getenv("port")
database = os.getenv("database")

connection_string = f"postgres:{password}@{url}:{port}/{database}"
engine = create_engine(f'postgresql://{connection_string}')

Base = automap_base()
Base.prepare(autoload_with=engine)
Inventory = Base.classes.inventory

@app.route("/")
def index():
    """Returns Homepage"""
    return render_template("index.html")

@app.route("/inventory")
def inventory():
    """Returns products available for purchase"""
    with Session(engine) as session:
        sel = [
            Inventory.name,
            Inventory.price,
            Inventory.size,
            Inventory.quantity,
            Inventory.image_url,
            Inventory.sku
        ]

        result = session.query(*sel).distinct().all()

        inventory_list = [
            {
                "name": row[0],
                "price": float(row[1]),
                "size": row[2],
                "quantity": row[3],
                "image_url": row[4],
                "sku": row[5],
            }
            for row in result
        ]

    return jsonify(inventory_list)

@app.route('/inventory/<id>', methods=['PUT'])
def update_inventory(id):
    with Session(engine) as session:
        inventory_item = session.query(Inventory).filter_by(id=id).first()

        updates = {
            'name': request.json.get('name'),
            'price': request.json.get('price'),
            'size': request.json.get('size'),
            'quantity': request.json.get('quantity'),
            'image_url': request.json.get('image_url'),
            'sku': request.json.get('sku')
        }

        report = []

        for key, value in updates.items():
            if value is not None and getattr(inventory_item, key) != value:
                if key == "price":
                    report.append(f"{key.capitalize()} changed from ${getattr(inventory_item, key)} to ${value:.2f}")
                else:
                    report.append(f"{key.capitalize()} changed from {getattr(inventory_item, key)} to {value}")
                setattr(inventory_item, key, value)

        session.commit()

    return jsonify(report)

if __name__ == "__main__":
    app.run(debug=True)