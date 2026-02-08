from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

planet = Blueprint('planet', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response


# Add or edit a planet
@planet.route('/planets', methods=['POST', 'PUT', 'DELETE'])
def add_or_update_planet():
    if request.method == 'POST':
        planet_data = request.get_json()
        query = '''
            INSERT INTO Planet (PlanetName, PlanetType, Mass, NumMoons, Eccentricity, Inclination) 
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                planet_data['PlanetName'],
                planet_data['PlanetType'],
                planet_data['Mass'],
                planet_data['NumMoons'],
                planet_data['Eccentricity'],
                planet_data['Inclination']
            ))
            db.get_db().commit()
            return jsonify({'message': 'Planet inserted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        planet_data = request.get_json()
        query = '''
            UPDATE Planet
            SET PlanetName = %s,
                PlanetType = %s,
                Mass = %s,
                NumMoons = %s,
                Eccentricity = %s,
                Inclination = %s
            WHERE PlanetID = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                planet_data['PlanetName'],
                planet_data['PlanetType'],
                int(planet_data['Mass']),
                int(planet_data['NumMoons']),
                float(planet_data['Eccentricity']),
                float(planet_data['Inclination']),
                int(planet_data['PlanetID'])
            ))
            db.get_db().commit()
            return jsonify({
                'message': 'Planet updated successfully',
                'rows_affected': cursor.rowcount
            }), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'DELETE':
        planet_id = request.args.get('PlanetID')
        return run_program(f'''
            DELETE FROM Planet
            WHERE PlanetID = {planet_id}
        ''')


# Get/add/update/delete planets that orbit a specified star
@planet.route('/planets/orbits', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_planets_that_orbit_star():
    if request.method == 'GET':
        star_identifier = request.args.get('star')
        cursor = db.get_db().cursor()

        if star_identifier.isnumeric():
            query = '''
                    SELECT S.StarName AS 'MainStar', S.StarID, P.PlanetID, P.PlanetName, O.OrbitalPeriod, O.SemiMajorAxis
                    FROM Star S JOIN Orbits O on S.StarID = O.StarID
                                JOIN Planet P on O.PlanetID = P.PlanetID
                    WHERE S.StarID = %s
                '''
            cursor.execute(query, star_identifier)
        else:
            query = '''
                    SELECT S.StarName AS 'MainStar', S.StarID, P.PlanetID, P.PlanetName, O.OrbitalPeriod, O.SemiMajorAxis
                    FROM Star S JOIN Orbits O on S.StarID = O.StarID
                                JOIN Planet P on O.PlanetID = P.PlanetID
                    WHERE S.StarName LIKE %s
                '''
            cursor.execute(query, (f"%{star_identifier}%",))

        try:
            theData = cursor.fetchall()
            response = make_response(jsonify(theData))
            response.status_code = 200
            db.get_db().commit()
            return response
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'POST':
        orbit_data = request.get_json()
        query = '''
            INSERT INTO Orbits (PlanetID, StarID, OrbitalPeriod, SemiMajorAxis) 
            VALUES (%s, %s, %s, %s)
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                orbit_data['PlanetID'],
                orbit_data['StarID'],
                orbit_data['OrbitalPeriod'],
                orbit_data['SemiMajorAxis']
            ))
            db.get_db().commit()
            return jsonify({'message': 'Orbital information inserted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        orbit_data = request.get_json()
        query = '''
            UPDATE Orbits
            SET StarID = %s,
                OrbitalPeriod = %s,
                SemiMajorAxis = %s
            WHERE PlanetID = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                orbit_data['StarID'],
                orbit_data['OrbitalPeriod'],
                orbit_data['SemiMajorAxis'],
                orbit_data['PlanetID']
            ))
            db.get_db().commit()
            return jsonify({
                'message': 'Orbital information updated successfully',
                'rows_affected': cursor.rowcount
            }), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'DELETE':
        orbit_data = request.get_json()
        query = '''
            DELETE FROM Orbits
            WHERE PlanetID = %s AND StarID = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                int(orbit_data['PlanetID']),
                int(orbit_data['StarID'])
            ))
            db.get_db().commit()
            return jsonify({'message': 'Orbital information deleted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400


# Get a planet info by ID
@planet.route('/planets/<int:PlanetID>', methods=['GET'])
def get_planets_by_id(PlanetID):
    query = f'''
        SELECT P.PlanetID, P.PlanetName, P.PlanetType, P.Mass, P.NumMoons, P.Eccentricity, P.Inclination, S.StarID
        FROM Planet P 
            LEFT JOIN Orbits O ON P.PlanetID = O.PlanetID
            LEFT JOIN Star S ON S.StarID = O.StarID
        WHERE P.PlanetID = {PlanetID}
    '''
    return run_program(query)


# Get a planet info by name
@planet.route('/planets/<PlanetName>', methods=['GET'])
def get_planets_by_name(PlanetName):
    query = f'''
        SELECT P.PlanetID, P.PlanetName, P.PlanetType, P.Mass, P.NumMoons, P.Eccentricity, P.Inclination, S.StarID
        FROM Planet P 
            LEFT JOIN Orbits O ON P.PlanetID = O.PlanetID
            LEFT JOIN Star S ON S.StarID = O.StarID
        WHERE PlanetName LIKE '%{PlanetName}%'
    '''
    return run_program(query)
