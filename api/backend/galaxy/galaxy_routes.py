from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

galaxy = Blueprint('galaxy', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response


# Do stuff with galaxies
@galaxy.route('/galaxies', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_galaxies():
    if request.method == 'GET':
        amount = request.args.get('amount')
        query = f'''
            SELECT * 
            FROM Galaxy
            LIMIT {amount}
        '''
        return run_program(query)

    elif request.method == 'POST':
        data = request.get_json()
        query = '''
            INSERT INTO Galaxy (GalaxyName, Redshift, YearDiscovered, SolarMassTrillions, DominantElement)
            VALUES (%s, %s, %s, %s, %s)
            '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                data['GalaxyName'],
                data['Redshift'],
                data['YearDiscovered'],
                data['SolarMassTrillions'],
                data['DominantElement']
            ))
            db.get_db().commit()
            return jsonify({'message': 'Galaxy inserted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        data = request.get_json()
        query = '''
            UPDATE Galaxy
            SET GalaxyName = %s,
                Redshift = %s,
                YearDiscovered = %s,
                SolarMassTrillions = %s,
                DominantElement = %s
            WHERE GalaxyID = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                data['GalaxyName'],
                float(data['Redshift']),
                data['YearDiscovered'],
                int(data['SolarMassTrillions']),
                data['DominantElement'],
                data['GalaxyID']
            ))
            db.get_db().commit()
            return jsonify({
                'message': 'Galaxy updated successfully',
                'rows_affected': cursor.rowcount
            }), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'DELETE':
        galaxy_id = request.args.get('GalaxyID')
        query = '''
            DELETE FROM Galaxy
            WHERE GalaxyID = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, galaxy_id)
            db.get_db().commit()
            return jsonify({'message': 'Galaxy deleted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400


# Get names of galaxies
@galaxy.route('/galaxies/names', methods=['GET'])
def get_galaxy_names():
    query = '''
        SELECT GalaxyName
        FROM Galaxy
        LIMIT 10
        '''
    return run_program(query)


# Get specific info of a galaxy from galaxy name
@galaxy.route('/galaxies/<GalaxyName>', methods=['GET'])
def find_galaxy_by_name(GalaxyName):
    query = f'''
        SELECT *
        FROM Galaxy
        WHERE GalaxyName LIKE '%{GalaxyName}%'
        '''
    return run_program(query)


# Get specific info of a galaxy from galaxy ID
@galaxy.route('/galaxies/<int:GalaxyID>', methods=['GET'])
def find_galaxy_by_id(GalaxyID):
    query = f'''
        SELECT * 
        FROM Galaxy
        WHERE GalaxyID = {GalaxyID}
    '''
    return run_program(query)


# Get all star systems in a galaxy by galaxy name
@galaxy.route('/galaxies/<GalaxyName>/starsystems', methods=['GET'])
def find_starsystems_by_galaxy_name(GalaxyName):
    query = f'''
        SELECT S.SystemName
        FROM StarSystem S JOIN Galaxy G on S.GalaxyID = G.GalaxyID
        WHERE G.GalaxyName LIKE '%{GalaxyName}%'
        '''
    return run_program(query)
