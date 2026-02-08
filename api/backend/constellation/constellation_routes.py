from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

constellation = Blueprint('constellation', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response



@constellation.route('/constellation', methods=['GET'])
def get_constellation():
    query = '''
        SELECT *
        FROM Constellation
    '''
    return run_program(query)


@constellation.route('/constellation/<ConstID>', methods=['GET'])
def get_constellation_info(ConstID):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.ConstID = {ConstID}
    '''
    return run_program(query)


@constellation.route('/constellation/star/<StarName>', methods=['GET'])
def get_constellation_from_star(StarName):
    query = f'''
        SELECT C.ConstName
        FROM Constellation C JOIN Star S ON C.ConstID = S.ConstID
        WHERE S.StarName = '{StarName}'
    '''
    return run_program(query)

@constellation.route('/constellation/<ConstID>/stars', methods=['GET'])
def get_from_star(ConstID):
    query = f'''
        SELECT S.StarName
        FROM Constellation C JOIN Star S ON C.ConstID = S.ConstID
        WHERE S.ConstID = {ConstID}
    '''
    return run_program(query)


@constellation.route('/constellation/brightestStar', methods=['GET'])
def get_brightest_star():
    query = f'''
        SELECT C.ConstName, S.StarName
        FROM Constellation C JOIN Star S ON C.BrightestStar = S.StarName;
    '''
    return run_program(query)


@constellation.route('/constellation/bestViewingMonth', methods=['GET'])
def find_const_best_view():
    query = f'''
        SELECT Constellation.BestViewingMonth
        FROM Constellation
    '''
    return run_program(query)


@constellation.route('/constellation/bestViewingMonth/<bestViewingMonth>', methods=['GET'])
def get_const_best_view(bestViewingMonth):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.BestViewingMonth = {bestViewingMonth}
    '''
    return run_program(query)


@constellation.route('/constellation/hemisphere', methods=['GET'])
def find_const_hemisphere():
    query = f'''
        SELECT Constellation.Hemisphere 
        FROM Constellation
    '''
    return run_program(query)


@constellation.route('/constellation/hemisphere/<Hemisphere>', methods=['GET'])
def get_const_hemisphere(Hemisphere):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.Hemisphere = {Hemisphere}
    '''
    return run_program(query)


@constellation.route('/constellation/name', methods=['GET'])
def const_by_name():
    query = f'''
        SELECT Constellation.ConstName
        FROM Constellation
    '''
    return run_program(query)


@constellation.route('/constellation/name/<ConstName>', methods=['GET'])
def get_const_by_name(ConstName):
    query = f'''
        SELECT * 
        FROM Constellation
        WHERE Constellation.ConstName= {ConstName}
    '''
    return run_program(query)
