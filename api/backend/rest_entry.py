from flask import Flask

from backend.db_connection import db

from backend.astronauts.astronauts_routes import astronauts
from backend.constellation.constellation_routes import constellation
from backend.findings.findings_routes import findings
from backend.galaxy.galaxy_routes import galaxy
from backend.missions.missions_routes import mission
from backend.spacecraft.spacecraft_routes import spacecraft
from backend.star_systems.star_system_routes import star_system
from backend.stars.star_routes import star
from backend.planets.planet_routes import planet

import os
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')
    app.register_blueprint(astronauts, web_prefix="/astronaut")
    app.register_blueprint(mission, web_prefix="/mission")
    app.register_blueprint(constellation, web_prefix="/constellation")
    app.register_blueprint(findings, web_prefix="/findings")
    app.register_blueprint(galaxy, web_prefix="/galaxy")
    app.register_blueprint(spacecraft, web_prefix="/spacecraft")
    app.register_blueprint(star_system, web_prefix="/star_system")
    app.register_blueprint(star, web_prefix="/star")
    app.register_blueprint(planet, web_prefix="/planet")

    # Don't forget to return the app object
    return app
