from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

star = Blueprint('star', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response


# Add, update, or delete stars
@star.route('/stars', methods=['POST', 'PUT', 'DELETE'])
def add_or_update_stars():
    if request.method == 'POST':
        data = request.get_json()
        query = '''
            INSERT INTO Star (SystemID, ConstID, StarName, Mass, Temperature, SpectralType) 
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                int(data['SystemID']),
                data['ConstID'],
                data['StarName'],
                data['Mass'],
                data['Temperature'],
                data['SpectralType']
            ))
            db.get_db().commit()
            return jsonify({'message': 'Star System inserted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'PUT':
        data = request.get_json()
        query = '''
            UPDATE Star
            SET SystemID = %s,
                ConstID = %s,
                StarName = %s,
                Mass = %s,
                Temperature = %s,
                SpectralType = %s
            WHERE StarID = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, (
                int(data['SystemID']),
                int(data['ConstID']),
                data['StarName'],
                int(data['Mass']),
                int(data['Temperature']),
                data['SpectralType'],
                int(data['StarID'])
            ))
            db.get_db().commit()
            return jsonify({
                'message': 'Star updated successfully',
                'rows_affected': cursor.rowcount
            }), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400

    elif request.method == 'DELETE':
        star_id = request.args.get('StarID')
        query = '''
            DELETE FROM Star
            WHERE StarID = %s
        '''

        try:
            cursor = db.get_db().cursor()
            cursor.execute(query, star_id)
            db.get_db().commit()
            return jsonify({'message': 'Star deleted successfully'}), 200
        except Exception as e:
            db.get_db().rollback()
            return jsonify({'error': str(e)}), 400


# Find star based on star system name
@star.route('/star_systems/<SystemName>', methods=['GET'])
def get_stars_by_system_name(SystemName):
    query = f'''
        SELECT StarName, StarID
        FROM Star S JOIN StarSystem SS ON S.SystemID = SS.SystemID
        WHERE SS.SystemName LIKE '%{SystemName}%'
    '''
    return run_program(query)


# Find star based on star system id
@star.route('/star_systems/<int:SystemID>', methods=['GET'])
def get_stars_by_system_id(SystemID):
    query = f'''
        SELECT Star.StarName, Star.StarID
        FROM Star
        WHERE Star.SystemID = {SystemID}
    '''
    return run_program(query)

# Find distInLY based on star system id
@star.route('/star_systems/<int:SystemID>', methods=['GET'])
def get_DLY_by_system_id(SystemID):
    query = f'''
        SELECT Star.StarName, Star.StarID
        FROM Star
        WHERE Star.SystemID = {SystemID}
    '''
    return run_program(query)


# Get info on a specific star
@star.route('/stars/<StarID>', methods=['GET'])
def get_star_info(StarID):
    query = f'''
        SELECT *
        FROM Star
        WHERE StarID = {StarID}
    '''
    return run_program(query)
