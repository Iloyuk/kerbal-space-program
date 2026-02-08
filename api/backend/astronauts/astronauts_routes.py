from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

astronauts = Blueprint('astronauts', __name__)

def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response

@astronauts.route('/astronauts', methods=['GET'])
def get_astronaut():
    query = '''
        SELECT * 
        FROM Astronaut
    '''
    return run_program(query)


@astronauts.route('/astronauts/<AstroID>', methods=['GET'])
def get_astronaut_info(AstroID):
    query = f'''
        SELECT * 
        FROM Astronaut
        WHERE Astronaut.AstroID = {AstroID}
    '''
    return run_program(query)

@astronauts.route('/astronauts', methods=['POST'])
def add_astro():
    astro_info = request.json
    name = astro_info['Name']
    country = astro_info['Country']
    yrinspace = astro_info['YearsInSpace']
    query = f'''
        INSERT INTO Astronaut(Name, Country, YearsInSpace)
        VALUES ("{name}","{country}",{yrinspace})
    '''
    return run_program(query)

@astronauts.route('/astronauts/<AstroID>', methods=['DELETE'])
def delete_astronaut(AstroID):
    query = f'''
        DELETE FROM Astronaut
        WHERE Astronaut.AstroID = {AstroID}
    '''
    return run_program(query)

@astronauts.route('/astronauts/<AstroID>/name/<Name>', methods=['PUT'])
def update_astronaut_name(AstroID, Name):
    query = f'''
        UPDATE Astronaut
        SET Name = "{Name}"
        WHERE Astronaut.AstroID = {AstroID}
    '''
    return run_program(query)

@astronauts.route('/astronauts/<AstroID>/country/<Country>', methods=['PUT'])
def update_astronaut_country(AstroID, Country):
    query = f'''
        UPDATE Astronaut
        SET Country = "{Country}"
        WHERE Astronaut.AstroID = {AstroID}
    '''
    return run_program(query)

@astronauts.route('/astronauts/<AstroID>/yearsinspace/<YearsInSpace>', methods=['PUT'])
def update_astronaut_yrs(AstroID, YearsInSpace):
    query = f'''
        UPDATE Astronaut
        SET YearsInSpace = {YearsInSpace}
        WHERE Astronaut.AstroID = {AstroID}
    '''
    return run_program(query)

@astronauts.route('/astronauts/name/<AstroName>', methods=['GET'])
def get_astronaut_by_name(AstroName):
    query = f'''
        SELECT * 
        FROM Astronaut
        WHERE Astronaut.Name = {AstroName}
    '''
    return run_program(query)


@astronauts.route('/astronauts/onShip/<ShipID>', methods=['GET'])
def get_astronauts_on_ship(ShipID):
    query = f'''
        SELECT Astronaut.Name, Astronaut.AstroID
        FROM SpacecraftAstronaut
        NATURAL JOIN Astronaut
        WHERE SpacecraftAstronaut.ShipID = {ShipID}
    '''
    return run_program(query)

@astronauts.route('/astronauts/onMission', methods=['GET'])
def get_astronaut_on_mission():
    query = '''
        SELECT A.Name, M.MissionName, M.Objective
        FROM Astronaut A
        JOIN MissionAstronaut MA on A.AstroID = MA.AstroID
        JOIN Mission M on MA.MissionID = M.MissionID
        JOIN StarSystemMissions SSM on MA.MissionID = SSM.MissionID
        WHERE SSM.EndDate IS NULL;
    '''
    return run_program(query)

@astronauts.route('/astronauts/<AstroID>/missions', methods=['GET'])
def get_astro_on_mission(AstroID):
    query = f'''
        SELECT DISTINCT Astronaut.AstroID, Mission.MissionName, Astronaut.Name, Mission.Objective, Mission.SuccessRating
        FROM MissionAstronaut
        JOIN Astronaut ON MissionAstronaut.AstroID = Astronaut.AstroID
        JOIN Mission ON MissionAstronaut.MissionID = Mission.MissionID
        WHERE Astronaut.AstroID = {AstroID}
    '''
    return run_program(query)

@astronauts.route('/astronauts/missions/<MissionID>', methods=['GET'])
def get_astro_on_spec_mission(MissionID):
    query = f'''
        SELECT DISTINCT Astronaut.AstroID, Mission.MissionName, Astronaut.Name, Mission.Objective, Mission.SuccessRating
        FROM MissionAstronaut
        JOIN Astronaut ON MissionAstronaut.AstroID = Astronaut.AstroID
        JOIN Mission ON MissionAstronaut.MissionID = Mission.MissionID
        WHERE Mission.MissionID = {MissionID}
    '''
    return run_program(query)