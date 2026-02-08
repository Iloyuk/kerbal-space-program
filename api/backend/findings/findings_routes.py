from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

findings = Blueprint('findings', __name__)


def run_program(query):
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    db.get_db().commit()
    return response


@findings.route('/findings', methods=['GET'])
def get_finding():
    query = '''
        SELECT * 
        FROM Finding
    '''
    return run_program(query)


@findings.route('/findings/<FindingID>', methods=['GET'])
def get_finding_info(FindingID):
    query = f'''
        SELECT * 
        FROM Finding
        WHERE FindingID = {FindingID}
    '''
    return run_program(query)


@findings.route('/findings/significance', methods=['GET'])
def finding_high_sig():
    query = f'''
        SELECT M.MissionName, M.Objective, F.FindingDate, F.Notes, F.Significance
        FROM Mission M
            JOIN MissionFinding MF ON M.MissionID = MF.MissionID
            JOIN Finding F ON MF.FindingID = F.FindingID
        '''
    return run_program(query)


@findings.route('/findings/significance/<Significance>', methods=['GET'])
def get_finding_high_sig (Significance):
    query = f'''
        SELECT M.MissionName, M.Objective, F.FindingDate, F.Notes
        FROM Mission M
            JOIN MissionFinding MF ON M.MissionID = MF.MissionID
            JOIN Finding F ON MF.FindingID = F.FindingID
        WHERE F.Significance = "{(Significance)}"
        '''
    return run_program(query)

@findings.route('/findings/<FindingID>/Sig/<Significance>', methods=['PUT'])
def update_finding_status(FindingID, Significance):
    query = f'''
        UPDATE Finding
        SET Finding.Significance = "{Significance}"
        WHERE Finding.FindingID = {FindingID}
        
    '''
    return run_program(query)


@findings.route('/findings/<FindingID>/Notes/<Notes>', methods=['PUT'])
def update_finding_notes(FindingID, Notes):
    query = f'''
        UPDATE Finding
        SET Finding.Notes = "{Notes}"
        WHERE Finding.FindingID = {FindingID};
    '''
    return run_program(query)

@findings.route('/findings', methods=['POST'])
def add_finding():
    finding_info = request.json
    sig = finding_info['Significance']
    findDate = finding_info['FindingDate']
    notes = finding_info['Notes']
    query = f'''
    INSERT INTO Finding(Significance, FindingDate, Notes)
    VALUES ("{sig}", "{findDate}","{notes}");
    '''
    return run_program(query)

