from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

spacecraft = Blueprint('spacecraft', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response


@spacecraft.route('/spacecraft', methods=['GET'])
def get_spacecraft():
    query = '''
        SELECT * 
        FROM Spacecraft
    '''
    return run_program(query)


@spacecraft.route('/spacecraft/status', methods=['GET'])
def get_spacecraft_status():
    query = '''
        SELECT Spacecraft.Status
        FROM Spacecraft
    '''
    return run_program(query)


@spacecraft.route('/spacecraft/status/<Status>', methods=['GET'])
def get_spacecraft_spec_status(Status):
    query = f'''
        SELECT *
        FROM Spacecraft
        WHERE Spacecraft.Status = {Status}
    '''
    return run_program(query)


@spacecraft.route('/spacecraft/<ShipID>/<Status>', methods=['PUT'])
def update_spacecraft_spec_status(ShipID, Status):
    query = f'''
        UPDATE Spacecraft
        SET Status = {Status}
        WHERE ShipID = {ShipID}
    '''
    return run_program(query)


@spacecraft.route('/spacecraft/<ShipID>', methods=['GET'])
def get_spacecraft_info(ShipID):
    query = f'''
        SELECT * 
        FROM Spacecraft
        WHERE Spacecraft.ShipID = {ShipID}
    '''
    return run_program(query)


@spacecraft.route('/spacecraft/<ShipID>', methods=['POST'])
def add_spacecraft(ShipID):
    ship_info = request.json

    shipID = {(ShipID)}
    shipName = ship_info['ShipName']
    status = ship_info['Status']
    mass = ship_info['Mass']
    manufacturer = ship_info['Manufacturer']
    capacity = ship_info['Capacity']

    query = f'''
    INSERT INTO Spacecraft (ShipID, ShipName, Status, Mass, Manufacturer, Capacity)
    VALUES ({shipID}, {shipName}, {status}, {mass}, {manufacturer}, {capacity})
    '''
    return run_program(query)


@spacecraft.route('/spacecraft/<ShipID>', methods=['PUT'])
def update_spacecraft(ShipID):
    ship_info = request.json
    return "Success"


@spacecraft.route('/spacecraft/<ShipID>/parts', methods=['GET'])
def get_spacecraft_parts(ShipID):
    query = f'''
        SELECT * 
        FROM Part
        WHERE Part.ShipID = {ShipID}
    '''
    return run_program(query)

@spacecraft.route('/spacecraft/<ShipID>/parts', methods=['POST'])
def add_spacecraft_parts(ShipID):
    data = request.json
    partName = data['PartName']
    mass = data['MassInTons']
    length = data['LengthInCM']
    usage = data['PartUsage']
    query = f'''
        INSERT INTO Part(ShipID, PartName, MassInTons, LengthInCM, PartUsage)
        VALUES ({ShipID},"{partName}",{mass},{length},"{usage}") 
    '''
    return run_program(query)

@spacecraft.route('/spacecraft/<ShipID>/parts/<PartID>', methods=['GET'])
def get_spacecraft_parts_info(ShipID, PartID):
    query = f'''
        SELECT * 
        FROM Part
        WHERE Part.ShipID = {ShipID} AND Part.PartID = {PartID}
    '''
    return run_program(query)

@spacecraft.route('/spacecraft/<ShipID>/parts/<PartID>', methods=['PUT'])
def update_part(ShipID, PartID):
    part_info = request.json
    return "Success"
