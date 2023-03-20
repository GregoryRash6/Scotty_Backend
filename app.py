import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify, render_template, redirect, request, abort
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

password = os.getenv("password")
url = os.getenv("url")
port = os.getenv("port")
database = os.getenv("database")
api_key = os.getenv("api_key")

connection_string = f"postgres:{password}@{url}:{port}/{database}"
engine = create_engine(f'postgresql://{connection_string}')

Base = automap_base()
Base.prepare(autoload_with=engine)
Inventory = Base.classes.inventory


@app.before_request
def require_api_key():
    if request.endpoint in ['update_inventory', 'add_inventory', 'delete_inventory/<id>']:
        key = request.headers.get('api_key')
        if key != api_key:
            abort(401, 'Unauthorized')


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
            Inventory.sku,
            Inventory.id
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
                "id": row[6],
            }
            for row in result
        ]

    return jsonify(inventory_list)


@app.route('/inventory/<id>', methods=['GET'])
def get_inventory_item(id):
    with Session(engine) as session:
        inventory_item = session.query(Inventory).filter_by(id=id).first()

        if inventory_item:
            item_info = {
                'id': inventory_item.id,
                'name': inventory_item.name,
                'price': float(inventory_item.price),
                'size': inventory_item.size,
                'quantity': inventory_item.quantity,
                'image_url': inventory_item.image_url,
                'sku': inventory_item.sku
            }

            return jsonify(item_info)

        else:
            return jsonify({'error': 'Item not found'}), 404


@app.route('/update_inventory/<id>', methods=['PATCH'])
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

        report = {}

        for key, value in updates.items():
            if value is not None and getattr(inventory_item, key) != value:
                report[key] = {
                    'old_value': getattr(inventory_item, key),
                    'new_value': value
                }
                setattr(inventory_item, key, value)

        session.commit()

        updated_item = {
            'id': inventory_item.id,
            'name': inventory_item.name,
            'price': float(inventory_item.price),
            'size': inventory_item.size,
            'quantity': inventory_item.quantity,
            'image_url': inventory_item.image_url,
            'sku': inventory_item.sku
        }
        updated_item.update(report)

    return jsonify(updated_item)


@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    with Session(engine) as session:
        new_item = Inventory(
            name=request.json['name'],
            price=request.json['price'],
            size=request.json['size'],
            quantity=request.json['quantity'],
            image_url=request.json['image_url'],
            sku=request.json['sku']
        )
        session.add(new_item)
        session.commit()

        added_item = {
            'id': new_item.id,
            'name': new_item.name,
            'price': float(new_item.price),
            'size': new_item.size,
            'quantity': new_item.quantity,
            'image_url': new_item.image_url,
            'sku': new_item.sku
        }

    return jsonify(added_item)


@app.route('/delete_inventory/<id>', methods=['DELETE'])
def delete_inventory(id):
    with Session(engine) as session:
        inventory_item = session.query(Inventory).filter_by(id=id).first()

        if inventory_item is None:
            return jsonify({'error': 'Item not found!'}), 404

        deleted_product = {
            'id': inventory_item.id,
            'name': inventory_item.name,
            'price': float(inventory_item.price),
            'size': inventory_item.size,
            'quantity': inventory_item.quantity,
            'image_url': inventory_item.image_url,
            'sku': inventory_item.sku
        }

        session.delete(inventory_item)
        session.commit()

    return jsonify(deleted_product)


if __name__ == "__main__":
    app.run(debug=True)
