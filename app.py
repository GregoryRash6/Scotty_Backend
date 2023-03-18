# Import Dependencies
import os
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify, render_template, redirect, request
from dotenv import load_dotenv

# Create Instance of Flask App
app = Flask(__name__)

# Load Dot Env
load_dotenv()

# Save Password
password = os.getenv("password")

url = os.getenv("url")

port = os.getenv("port")

database = os.getenv("database")

# Set Connection String
connection_string = f"postgres:{password}@{url}:{port}/{database}"

# Set Engine
engine = create_engine(f'postgresql://{connection_string}')

# create the base and prepare the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save References to Table
Inventory = Base.classes.inventory

# # Create Session
session = Session(engine)


# Create Home Route
@app.route("/")
# Define Index Function
def index():
    """Returns Homepage"""

    # Render Template
    return render_template("index.html")


# Create Dates Route
@app.route("/inventory")
# Define Dates Function
def dates():
    """Returns products available for purchase"""

    sel = [
        Inventory.name,
        Inventory.price,
        Inventory.size,
        Inventory.quantity,
        Inventory.image_url
    ]

    # Perform SQL Query
    result = session.query(*sel)\
    .distinct()\
    .all()
    
    inventory = []

    for x in range(len(result)):
        inventory.append({
            "name": result[x][0],
            "price": float(result[x][1]),
            "size": result[x][2],
            "quantity": result[x][3],
            "image_url": result[x][4],
        })
    
    return jsonify(inventory)

@app.route('/inventory/<id>', methods=['PUT'])
def update_inventory(id):
    session = Session(engine)
    
    # get request data
    new_quantity = request.json['quantity']
    
    # get inventory item by id
    inventory_item = session.query(Inventory).filter_by(id=id).first()
    
    # update inventory item properties
    inventory_item.quantity = new_quantity
    
    # commit changes and close session
    session.commit()
    session.close()
    
    return 'Inventory Updated'
    

if __name__ == "__main__":
    app.run(debug=True)