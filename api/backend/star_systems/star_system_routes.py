from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

star_system = Blueprint('star_system', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response


# Get all star systems in a galaxy by galaxy id
@star_system.route('/galaxies/<int:GalaxyID>/starsystems', methods=['GET', 'POST', 'PUT'])
def find_starsystems_by_galaxy_id(GalaxyID):
    if request.method == 'GET':
        query = f'''
            SELECT SystemName, SystemID
            FROM StarSystem
            WHERE GalaxyID = {GalaxyID}
        '''
        return run_program(query)

    elif request.method == 'POST':
        data = request.get_json()
        query = f'''
            INSERT INTO StarSystem (GalaxyID, SystemName, DistInLY, SystemType, NumStars)
            VALUES ({GalaxyID}, '{data['SystemName']}', {data['DistInLY']}, '{data['SystemType']}', {data['NumStars']})
            '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query)
            db.get_db().commit()
            return jsonify({'message': 'Star System inserted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        data = request.get_json()
        query = f'''
            UPDATE StarSystem
            SET GalaxyID = {GalaxyID},
                SystemName = {data['SystemName']},
                DistInLY = {data['DistInLY']},
                SystemType = '{data['SystemType']}',
                NumStars = {data['NumStars']}
            WHERE SystemID = '{data['SystemID']}'
            '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query)
            db.get_db().commit()
            return jsonify({
                'message': 'Star system updated successfully',
                'rows_affected': cursor.rowcount
            }), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400


# Get or delete a star system by its id
@star_system.route('/starsystems/<int:SystemID>', methods=['GET', 'DELETE'])
def find_starsystems_by_starsystem_name(SystemID):
    if request.method == 'GET':
        query = f'''
            SELECT *
            FROM StarSystem
            WHERE SystemID = {SystemID}
        '''
        return run_program(query)

    elif request.method == 'DELETE':
        query = f'''
            DELETE FROM StarSystem
            WHERE SystemID = {SystemID}
        '''
        return run_program(query)


# Get a star system by a combination of galaxy name and star system name
@star_system.route('/galaxies/<GalaxyName>/starsystems/<SystemName>', methods=['GET'])
def find_starsystems_by_galaxy_name_and_starsystem_name(GalaxyName, SystemName):
    query = f'''
        SELECT *
        FROM StarSystem SS JOIN Galaxy G on SS.GalaxyID = G.GalaxyID
        WHERE G.GalaxyName LIKE '%{GalaxyName}%' AND SS.SystemName LIKE '%{SystemName}%'
    '''
    return run_program(query)


@star_system.route('/galaxies/<int:GalaxyID>/starsystems/distInLY', methods=["GET"])
def find_DIYL_in_ss(GalaxyID):
    query = f'''
        SELECT StarSystem.SystemID, StarSystem.DistInLY
        FROM StarSystem
        WHERE StarSystem.GalaxyID = {GalaxyID}
    '''
    return run_program(query)
