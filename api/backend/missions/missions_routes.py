from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

mission = Blueprint('mission', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response


@mission.route('/missions', methods=['GET'])
def get_mission():
    query = '''
        SELECT * FROM Mission NATURAL JOIN StarSystemMissions;
    '''
    return run_program(query)


@mission.route('/missions/name', methods=['GET'])
def get_missionname():
    query = '''
        SELECT Mission.MissionName FROM Mission NATURAL JOIN StarSystemMissions;
    '''
    return run_program(query)

@mission.route('/missions/extended', methods=['GET'])
def get_mission_extended_info():
    query = '''
        SELECT Mission.MissionName, Mission.Objective, StarSystemMissions.StartDate, StarSystemMissions.EndDate, StarSystem.SystemName, StarSystem.SystemID, Mission.MissionID
        FROM StarSystemMissions
        JOIN Mission ON StarSystemMissions.MissionID = Mission.MissionID
        JOIN StarSystem ON StarSystemMissions.SystemID = StarSystem.SystemID
    '''
    return run_program(query)


@mission.route('/missions/name/<MissionName>', methods=['GET'])
def get_mission_search(MissionName):
    query = f'''
        SELECT * FROM Mission
        WHERE Mission.MissionName = '{MissionName}';
    '''
    return run_program(query)


@mission.route('/missions/<MissionID>', methods=['GET'])
def get_mission_info(MissionID):
    query = f'''
        SELECT * 
        FROM Mission NATURAL JOIN StarSystemMissions;
        WHERE Mission.MissionID = {MissionID}
    '''
    return run_program(query)


@mission.route('/missions/objective', methods=['GET'])
def get_ongoing_missions():
    query = f'''
        SELECT Mission.Objective, Mission.MissionName, Mission.Agency
        FROM Mission
    '''
    return run_program(query)

@mission.route('/missions/<MissionID>/findings', methods=['GET'])
def get_findings_from_mission(MissionID):
    query = f'''
        SELECT Mission.MissionName, Mission.MissionID, Finding.*
        FROM MissionFinding 
        NATURAL JOIN Mission
        NATURAL JOIN Finding
        WHERE Mission.MissionID = {MissionID}
    '''
    return run_program(query)

@mission.route('/missions/<MissionID>/findings/<FindingID>', methods=['POST'])
def add_findings_mission(MissionID, FindingID):
    query = f'''
        INSERT INTO MissionFinding(MissionID, FindingID)
        VALUES ({MissionID},{FindingID})
    '''
    return run_program(query)

@mission.route('/missions/<MissionID>/status', methods=['PUT'])
def change_mission_status(MissionID):
    query = f'''
    UPDATE StarSystemMissions
    SET EndDate = now()
    WHERE StarSystemMissions.MissionID = {MissionID};

    '''
    return run_program(query)



@mission.route("/missions/<MissionID>/name/<Name>", methods=['PUT'])
def update_mission_name(MissionID,Name):
    query = f'''
        UPDATE Mission
        SET MissionName = "{Name}"
        WHERE MissionID = {MissionID}
    '''
    return run_program(query)


@mission.route("/missions/<MissionID>/agency/<Agency>", methods=['PUT'])
def update_mission_agency(MissionID,Agency):
    query = f'''
        UPDATE Mission
        SET Agency = "{Agency}"
        WHERE MissionID = {MissionID}
    '''
    return run_program(query)

@mission.route("/missions/<MissionID>/objective/<Objective>", methods=['PUT'])
def update_mission_obj(MissionID,Objective):
    query = f'''
        UPDATE Mission
        SET Objective = "{Objective}"
        WHERE MissionID = {MissionID}
    '''
    return run_program(query)

@mission.route("/missions/<MissionID>/status/<Status>", methods=['PUT'])
def update_mission_status(MissionID,Status):
    query = f'''
        UPDATE Mission
        SET MissionStatus = "{Status}"
        WHERE MissionID = {MissionID}
    '''
    return run_program(query)

@mission.route("/missions/<MissionID>/starsystem/startdate/<StartDate>", methods=['PUT'])
def update_mission_starsys_startdate(MissionID,StartDate):
    query = f'''
        UPDATE StarSystemMissions
        SET StartDate = "{StartDate}"
        WHERE MissionID = {MissionID}
    '''
    return run_program(query)

@mission.route("/missions/<MissionID>/starsystem/startdate/<EndDate>", methods=['PUT'])
def update_mission_starsys_enddate(MissionID,EndDate):
    query = f'''
        UPDATE StarSystemMissions
        SET EndDate = "{EndDate}"
        WHERE MissionID = {MissionID}
    '''
    return run_program(query)

@mission.route("/missions/<MissionID>/starsystem/<SystemID>", methods=['PUT'])
def update_mission_starsys_SystemID(MissionID,SystemID):
    query = f'''
        UPDATE StarSystemMissions
        SET SystemID = "{SystemID}"
        WHERE MissionID = {MissionID}
    '''
    return run_program(query)

@mission.route("/missions", methods=['POST'])
def add_mission():
    data = request.json
    MissionName = data['MissionName']
    Objective = data['Objective']
    Agency = data['Agency']
    SuccessRating = data['SuccessRating']

    query = f'''
        INSERT INTO Mission(MissionName, Objective, Agency, SuccessRating)
        VALUES ("{MissionName}", "{Objective}", "{Agency}", "{SuccessRating}")
    '''
    return run_program(query)

@mission.route("/missions/starsystem", methods=['POST'])
def add_mission_starsystem():
    data = request.json
    MissionID = data['MissionID']
    SystemID = data['SystemID']
    StartDate = data['StartDate']
    EndDate = data['EndDate']

    if EndDate == "None":
        query = f'''
            INSERT INTO StarSystemMissions(MissionID,SystemID,StartDate, EndDate)
            VALUES ({MissionID},{SystemID}, "{StartDate}", NULL)
        '''
    else:
        query = f'''
            INSERT INTO StarSystemMissions(MissionID,SystemID,StartDate, EndDate)
            VALUES ({MissionID},{SystemID}, "{StartDate}", "{EndDate}")
        '''
    return run_program(query)