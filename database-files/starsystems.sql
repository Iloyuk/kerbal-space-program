CREATE DATABASE IF NOT EXISTS NYASA;
USE NYASA;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Galaxy;
DROP TABLE IF EXISTS StarSystem;
DROP TABLE IF EXISTS Star;
DROP TABLE IF EXISTS Constellation;
DROP TABLE IF EXISTS StarSystemMissions;
DROP TABLE IF EXISTS Mission;
DROP TABLE IF EXISTS MissionSpacecraft;
DROP TABLE IF EXISTS Spacecraft;
DROP TABLE IF EXISTS MissionAstronaut;
DROP TABLE IF EXISTS SpacecraftAstronaut;
DROP TABLE IF EXISTS Part;
DROP TABLE IF EXISTS MissionFinding;
DROP TABLE IF EXISTS Finding;
DROP TABLE IF EXISTS Planet;
DROP TABLE IF EXISTS Orbits;
DROP TABLE IF EXISTS Astronaut;

SET FOREIGN_KEY_CHECKS = 1;

/*
 Create tables
 */
CREATE TABLE IF NOT EXISTS Galaxy (
    GalaxyID INT PRIMARY KEY AUTO_INCREMENT,
    GalaxyName VARCHAR(100) UNIQUE,
    Redshift DOUBLE,
    DateDiscovered date NOT NULL,
    SolarMassTrillions DOUBLE,
    DominantElement VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS StarSystem (
    SystemID INT PRIMARY KEY AUTO_INCREMENT,
    GalaxyID INT NOT NULL,
    SystemName VARCHAR(100) UNIQUE,
    DistInLY INT NOT NULL,
    SystemType ENUM('Binary','Multiple') NOT NULL,
    NumStars INT NOT NULL,
    FOREIGN KEY (GalaxyID) REFERENCES Galaxy(GalaxyID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Constellation (
    ConstID INT PRIMARY KEY AUTO_INCREMENT,
    ConstName VARCHAR(100) UNIQUE,
    Abbreviation VARCHAR(20) UNIQUE,
    Hemisphere ENUM('North', 'South') NOT NULL,
    BrightestStar VARCHAR(100) NOT NULL,
    BestViewingMonth ENUM('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec') NOT NULL,
    Notes VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS Finding (
    FindingID INT PRIMARY KEY AUTO_INCREMENT,
    Significance ENUM('Low', 'Medium', 'High') NOT NULL,
    FindingDate date NOT NULL,
    Notes VARCHAR(300) NOT NULL
);

CREATE TABLE IF NOT EXISTS Star (
    StarID INT PRIMARY KEY AUTO_INCREMENT,
    SystemID INT NOT NULL,
    ConstID INT,
    StarName VARCHAR(100) UNIQUE,
    Mass INT,
    Temperature INT,
    SpectralType VARCHAR(15) NOT NULL,
    FOREIGN KEY (SystemID) REFERENCES StarSystem(SystemID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (ConstID) REFERENCES Constellation(ConstID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Planet (
    PlanetID INT PRIMARY KEY AUTO_INCREMENT,
    PlanetName VARCHAR(100) UNIQUE,
    PlanetType VARCHAR(50) NOT NULL,
    Mass INT,
    NumMoons INT,
    Eccentricity DOUBLE,
    Inclination DOUBLE
);

CREATE TABLE IF NOT EXISTS Spacecraft (
    ShipID INT PRIMARY KEY AUTO_INCREMENT,
    ShipName VARCHAR(100) UNIQUE NOT NULL,
    Status ENUM('Under Construction', 'Operational', 'Decommissioned', 'Damaged') NOT NULL,
    Mass INT NOT NULL,
    Manufacturer VARCHAR(100) NOT NULL,
    Capacity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Part (
    PartID INT PRIMARY KEY AUTO_INCREMENT,
    ShipID INT NOT NULL,
    PartName VARCHAR(75) NOT NULL,
    MassInTons INT NOT NULL,
    LengthInCM INT NOT NULL,
    PartUsage VARCHAR(100) NOT NULL,
    FOREIGN KEY (ShipID) REFERENCES Spacecraft(ShipID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Mission (
    MissionID INT PRIMARY KEY AUTO_INCREMENT,
    MissionName VARCHAR(100) NOT NULL,
    Agency VARCHAR(30) NOT NULL,
    Objective VARCHAR(200) NOT NULL,
    SuccessRating ENUM('Low', 'Medium', 'High') NOT NULL
);

CREATE TABLE IF NOT EXISTS Astronaut (
    AstroID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    YearsInSpace INT NOT NULL
);

CREATE TABLE IF NOT EXISTS MissionSpacecraft (
    MissionID INT,
    ShipID INT,
    MissionStatus ENUM('Planned', 'Ongoing', 'Complete') NOT NULL,
    PRIMARY KEY (MissionID, ShipID),
    FOREIGN KEY (MissionID) REFERENCES Mission(MissionID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (ShipID) REFERENCES Spacecraft(ShipID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MissionAstronaut (
    MissionID INT,
    AstroID INT,
    PRIMARY KEY (MissionID, AstroID),
    FOREIGN KEY(MissionID) REFERENCES Mission(MissionID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY(AstroID) REFERENCES Astronaut(AstroID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MissionFinding(
    MissionID INT,
    FindingID INT,
    PRIMARY KEY (MissionID, FindingID),
    FOREIGN KEY (MissionID) REFERENCES Mission(MissionID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (FindingID) REFERENCES Finding(FindingID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS StarSystemMissions (
    SystemID INT,
    MissionID INT,
    StartDate date NOT NULL,
    EndDate date,
    PRIMARY KEY (SystemID, MissionID),
    FOREIGN KEY (SystemID) REFERENCES StarSystem(SystemID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (MissionID) REFERENCES Mission(MissionID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SpacecraftAstronaut (
    ShipID INT,
    AstroID INT,
    PRIMARY KEY (ShipID, AstroID),
    FOREIGN KEY(ShipID) REFERENCES Spacecraft(ShipID),
    FOREIGN KEY(AstroID) REFERENCES Astronaut(AstroID)
);

CREATE TABLE IF NOT EXISTS Orbits (
    PlanetID INT NOT NULL,
    StarID INT NOT NULL,
    OrbitalPeriod DOUBLE NOT NULL,
    SemiMajorAxis DOUBLE NOT NULL,
    PRIMARY KEY (PlanetID, StarID),
    FOREIGN KEY (PlanetID) REFERENCES Planet(PlanetID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (StarID) REFERENCES Star(StarID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


/*
 Insert data into tables
 */
-- GALAXY
INSERT INTO Galaxy (GalaxyName, Redshift, DateDiscovered, SolarMassTrillions, DominantElement)
VALUES 
('Milky Way', 0.0, '1610-01-01', 1.5, 'Hydrogen'),
('Andromeda', -0.001001, '0964-01-01', 1.23, 'Hydrogen'),
('Triangulum', 0.00096, '1764-01-01', 0.5, 'Helium'),
('Andromeda Galaxy', -0.001001, '0964-01-01', 1.5, 'Hydrogen'),
('Large Magellanic Cloud', 0.000934, '1500-01-01', 0.1, 'Hydrogen'),
('Small Magellanic Cloud', 0.000527, '1500-01-01', 0.07, 'Helium'),
('Triangulum Galaxy', 0.00096, '1764-08-25', 0.5, 'Hydrogen'),
('NGC 1300', 0.00526, '1835-03-04', 1.0, 'Oxygen'),
('NGC 6744', 0.00281, '1826-06-15', 1.4, 'Helium'),
('NGC 4414', 0.00367, '1865-09-10', 1.2, 'Hydrogen'),
('IC 1101', 0.077, '1790-11-12', 100.0, 'Iron'),
('NGC 4696', 0.00987, '1826-10-03', 2.1, 'Hydrogen'),
('NGC 6872', 0.0146, '1850-02-27', 1.6, 'Carbon');

-- STAR SYSTEM
INSERT INTO StarSystem (GalaxyID, SystemName, DistInLY, SystemType, NumStars)
VALUES
(1, 'Barnard’s Star System', 5, 'Binary', 1),
(1, 'Sirius System', 8, 'Binary', 2),
(2, 'M31 System Y', 2540001, 'Multiple', 3),
(3, 'M33-Kepler System', 2730000, 'Binary', 2),
(1, 'Alpha Centauri', 4, 'Multiple', 3),
(1, 'Proxima Centauri System', 4, 'Binary', 1),
(1, 'TRAPPIST-1 System', 40, 'Binary', 1),
(1, 'Epsilon Eridani System', 10, 'Binary', 1),
(1, 'Gliese 581 System', 20, 'Binary', 1),
(1, 'Tau Ceti System', 12, 'Binary', 1),
(1, 'Wolf 1061 System', 14, 'Binary', 1),
(1, 'Luyten’s Star System', 12, 'Binary', 1),
(1, 'Kapteyn’s Star System', 13, 'Binary', 1),
(1, 'Kepler-62 System', 1200, 'Multiple', 2),
(2, 'Kepler-186 System', 492, 'Multiple', 2),
(2, 'Kepler-22 System', 620, 'Binary', 1),
(3, 'OGLE-2005-BLG-390Lb Host', 21500, 'Binary', 1),
(4, 'PSR B1257+12 System', 2300, 'Binary', 1),
(1, 'LHS 1140 System', 49, 'Binary', 1),
(2, 'RX J0042.6+4115 System', 2520000, 'Binary', 2),
(2, 'Andromeda-V1 System', 2530000, 'Binary', 1),
(3, 'M33-X7 System', 3000000, 'Binary', 2),
(3, 'NGC 604 Region Cluster A', 3020000, 'Multiple', 7),
(4, 'HD 128311 System', 30000000, 'Binary', 1),
(4, 'HD 122563 System', 31000000, 'Binary', 1),
(5, 'ICX-01 SuperCluster Core', 110000000, 'Multiple', 5),
(5, 'ICX-Alpha Prime', 111000000, 'Binary', 2),
(6, 'NGC 1300-BH1 System', 61000000, 'Binary', 2),
(6, 'NGC 1300-Y7', 61500000, 'Multiple', 3);

-- CONSTELLATION
INSERT INTO Constellation (ConstName, Abbreviation, Hemisphere, BrightestStar, BestViewingMonth, Notes)
VALUES 
('Centaurus', 'Cen', 'South', 'Alpha Centauri', 'May', 'Home to the closest star system'),
('Cassiopeia', 'Cas', 'North', 'Schedar', 'Nov', 'Visible year-round in the Northern Hemisphere'),
('Orion', 'Ori', 'North', 'Rigel', 'Jan', 'One of the most recognizable constellations with the Orion Belt.'),
('Scorpius', 'Sco', 'South', 'Antares', 'Jul', 'Features a bright red supergiant star, Antares.'),
('Ursa Major', 'UMa', 'North', 'Alioth', 'Apr', 'Home to the Big Dipper asterism.'),
('Crux', 'Cru', 'South', 'Acrux', 'May', 'The smallest constellation, also known as the Southern Cross.'),
('Lyra', 'Lyr', 'North', 'Vega', 'Aug', 'Contains the bright star Vega and the Ring Nebula.'),
('Taurus', 'Tau', 'North', 'Aldebaran', 'Feb', 'Associated with the Pleiades and Hyades star clusters.'),
('Canis Major', 'CMa', 'South', 'Sirius', 'Feb', 'Home to Sirius, the brightest star in the night sky.'),
('Cygnus', 'Cyg', 'North', 'Deneb', 'Sep', 'Also known as the Northern Cross; part of the Summer Triangle.'),
('Sagittarius', 'Sgr', 'South', 'Kaus Australis', 'Aug', 'Contains the center of the Milky Way galaxy.');

-- STAR
INSERT INTO Star (SystemID, ConstID, StarName, Mass, Temperature, SpectralType)
VALUES
(5, 1, 'Alpha Centauri A', 1.1, 5790, 'G2'),
(5, 1, 'Alpha Centauri B', 0.9, 5260, 'K1'),
(5, 1, 'Proxima Centauri', 0.12, 3042, 'M5'),
(2, 9, 'Sirius A', 2.1, 9940, 'A1'),
(2, 9, 'Sirius B', 1.0, 25200, 'DA2'),
(1, 1, 'Barnards Star', 0.16, 3134, 'M4'),
(7, 7, 'TRAPPIST-1', 0.089, 2559, 'M8'),
(10, 8, 'Tau Ceti', 0.78, 5344, 'G8'),
(8, 1, 'Epsilon Eridani', 0.82, 5146, 'K2'),
(9, 1, 'Gliese 581', 0.31, 3200, 'M3'),
(11, 1, 'Wolf 1061', 0.25, 3305, 'M3'),
(12, 1, 'Luytens Star', 0.26, 3150, 'M3.5'),
(13, 1, 'Kapteyns Star', 0.28, 3550, 'M1'),
(14, 10, 'Kepler-62 A', 0.69, 4925, 'K2'),
(14, 10, 'Kepler-62 B', 0.21, 2900, 'M5'),
(15, 10, 'Kepler-186', 0.48, 3755, 'M1'),
(15, 10, 'Kepler-186b Host', 0.49, 3780, 'M1'),
(16, 10, 'Kepler-22', 0.97, 5518, 'G5'),
(17, 11, 'OGLE-2005-BLG-390Lb Star', 0.22, 3200, 'M4'),
(18, 11, 'PSR B1257+12', 1.4, 28000, 'NS'),
(19, 8, 'LHS 1140', 0.146, 3130, 'M4'),
(20, 2, 'RX J0042.6+4115', 3.2, 28000, 'B0'),
(21, 2, 'Andromeda-V1', 2.3, 8200, 'A2'),
(23, 3, 'M33 X-7 Primary', 70, 35000, 'O7'),
(23, 3, 'M33 X-7 Companion', 15.65, 26000, 'B1'),
(24, 3, 'NGC 604-A1', 20, 32000, 'O9'),
(24, 3, 'NGC 604-A2', 18, 29500, 'B0'),
(24, 3, 'NGC 604-A3', 16, 29000, 'B1'),
(25, 4, 'HD 128311 A', 0.84, 5000, 'K0'),
(27, 11, 'ICX-Alpha Prime A', 22.5, 32500, 'O9'),
(27, 11, 'ICX-Alpha Prime B', 19.0, 30000, 'B0'),
(29, 6, 'NGC 1300-BH1 Primary', 33, 31000, 'O8'),
(29, 6, 'NGC 1300-BH1 Companion', 20, 27000, 'B0');

-- PLANET
INSERT INTO Planet (PlanetName, PlanetType, Mass, NumMoons, Eccentricity, Inclination)
VALUES 
('Earth', 'Terrestrial', 5972, 1, 0.0167, 0.00005),
('Mars', 'Terrestrial', 641, 2, 0.0934, 1.850),
('Proxima b', 'Exoplanet', 1080, 0, 0.05, 0.0),
('Spiral-1b', 'Gas Giant', 19000, 16, 0.04, 2.3),
('Sombrero Prime', 'Rocky', 8500, 2, 0.08, 5.2),
('M87-ExoA', 'Ice Giant', 14800, 5, 0.1, 3.5),
('TRAPPIST-1e', 'Terrestrial', 0.692, 0, 0.005, 89.7),
('Kepler-186f', 'Terrestrial', 1.4, 0, 0.04, 89.9),
('Proxima c', 'Super-Earth', 1.27, 0, 0.35, 88.5),
('HD 209458 b', 'Hot Jupiter', 220, 0, 0.014, 86.1),
('Kepler-22b', 'Super-Earth', 36, 0, 0.13, 89.8),
('55 Cancri e', 'Lava World', 8.6, 0, 0.05, 83.4),
('Kepler-62f', 'Terrestrial', 2.8, 0, 0.05, 89.5),
('HD 189733 b', 'Hot Jupiter', 365, 0, 0.03, 85.7),
('LHS 1140 b', 'Super-Earth', 6.6, 0, 0.15, 88.2),
('Juno', 'Terrestrial', 0.02, 0, 0.26, 13.0),
('Vulcan', 'Terrestrial', 0.5, 0, 0.01, 0.5),
('Helios', 'Gas Giant', 318, 69, 0.048, 1.3),
('Hyperion', 'Ice Giant', 85, 14, 0.017, 0.8),
('Chroma', 'Ocean World', 4.2, 2, 0.12, 2.0);
-- ORBITS
INSERT INTO Orbits (PlanetID, StarID, OrbitalPeriod, SemiMajorAxis)
VALUES 
(1, 1, 365.25, 1.0),
(2, 1, 687, 1.52),
(3, 4, 11.2, 0.05),
(4, 6, 430, 0.9),
(5, 10, 380, 1.1),
(6, 7, 700, 2.2),
(7, 32, 0.74, 0.0156),
(8, 20, 267.3, 0.718),
(9, 33, 2.2, 0.031),
(10, 25, 24.7, 0.0875),
(11, 1, 1593.6, 2.67),
(12, 1, 12.3, 0.09),
(13, 1, 4332.6, 5.2),
(14, 1, 30687, 19.2),
(15, 2, 90.0, 0.6);

-- SPACECRAFT
INSERT INTO Spacecraft (ShipName, Status, Mass, Manufacturer, Capacity)
VALUES 
('Voyager I', 'Operational', 721, 'NASA', 0),
('Perseverance Rover', 'Operational', 1025, 'JPL', 0),
('Orion Crew Module', 'Operational', 26000, 'Lockheed Martin', 6),
('Kepler Explorer', 'Operational', 1400, 'NASA', 0),
('BlackHole Probe', 'Under Construction', 900, 'ESA', 0),
('Cosmic Cruiser', 'Operational', 34000, 'SpaceX', 8),
('Apollo 11', 'Decommissioned', 30300, 'NASA', 3),
('James Webb Space Telescope', 'Operational', 6200, 'NASA/ESA/CSA', 0),
('Starship HLS', 'Under Construction', 120000, 'SpaceX', 6),
('ExoMars Rover', 'Operational', 310, 'ESA/Roscosmos', 0),
('Artemis I Orion', 'Operational', 26000, 'NASA/ESA', 4),
('Dragon Endeavour', 'Operational', 12055, 'SpaceX', 4),
('Europa Clipper', 'Under Construction', 6000, 'NASA JPL', 0);

-- PART
INSERT INTO Part (ShipID, PartName, MassInTons, LengthInCM, PartUsage)
VALUES 
(1, 'Command Module Columbia', 5, 320, 'Crew cabin and reentry control'),
(1, 'Lunar Module Eagle', 15, 420, 'Moon landing and ascent stage'),
(1, 'Service Module Engine', 2, 260, 'Orbital maneuvering and power systems'),
(2, 'High-Gain Antenna', 0.1, 360, 'Interstellar communication'),
(2, 'RTG Power Supply', 0.3, 150, 'Power source via radioisotope decay'),
(2, 'Imaging Science Subsystem', 0.2, 100, 'Planetary and deep space imaging'),
(3, 'Primary Mirror Array', 2.4, 650, 'Infrared light collection'),
(3, 'Sunshield Layers', 0.5, 2100, 'Thermal protection for optics'),
(3, 'Cryocooler Unit', 0.2, 100, 'Infrared detector cooling system'),
(4, 'Main Propulsion Tank', 30, 1200, 'Methalox fuel storage'),
(4, 'Heat Shield Tiles', 5, 500, 'Thermal protection during reentry'),
(4, 'Lunar Cargo Bay', 10, 800, 'Payload delivery to lunar surface'),
(5, 'Drill Assembly', 0.15, 120, 'Subsurface soil sampling'),
(5, 'Analytical Laboratory Drawer', 0.08, 90, 'Onboard chemical analysis'),
(5, 'Solar Panels', 0.12, 140, 'Energy collection'),
(6, 'Crew Module', 8, 320, 'Human habitation and controls'),
(6, 'European Service Module', 10, 500, 'Power and propulsion for Orion'),
(6, 'Docking Adapter', 1, 120, 'Space station interface'),
(7, 'Trunk Section', 2, 400, 'Unpressurized cargo and solar arrays'),
(7, 'Heat Shield', 1.5, 320, 'Atmospheric reentry protection'),
(7, 'Launch Abort System', 1, 300, 'Emergency crew escape'),
(8, 'Radar for Ice Penetration', 0.4, 160, 'Analyze subsurface ice structures'),
(8, 'Thermal Emission Imaging System', 0.2, 110, 'Map surface temperature'),
(8, 'Magnetometer Boom', 0.3, 200, 'Detect magnetic field from ocean activity');

-- MISSION
INSERT INTO Mission (MissionName, Agency, Objective, SuccessRating)
VALUES 
('Voyager Interstellar Mission', 'NASA', 'Study outer solar system and interstellar space', 'High'),
('Mars 2020', 'NASA', 'Search for signs of ancient life on Mars', 'High'),
('Artemis I', 'NASA', 'Uncrewed lunar orbit mission to test Orion', 'Medium'),
('Kepler-Deep Search', 'NASA', 'Detect Earth-like planets in distant systems', 'High'),
('EventHorizon Chase', 'ESA', 'Map regions near supermassive black holes', 'Medium'),
('Stellar Drift', 'SpaceX', 'Crewed deep space test of long-range ship', 'High'),
('Apollo 11', 'NASA', 'First manned Moon landing and return', 'High'),
('JWST Launch Mission', 'NASA/ESA/CSA', 'Deploy space telescope to L2 orbit for deep space observation', 'High'),
('ExoMars Surface Mission', 'ESA/Roscosmos', 'Search for signs of life on Mars', 'Medium'),
('Europa Clipper Launch', 'NASA', 'Investigate Jupiter’s moon Europa for potential habitability', 'Medium'),
('Dragon ISS Supply Run', 'SpaceX', 'Resupply mission to the ISS', 'High'),
('Starship Lunar Test', 'SpaceX', 'Test reusable lunar lander system in lunar orbit', 'High');

-- ASTRONAUT
INSERT INTO Astronaut (Name, Country, YearsInSpace)
VALUES 
('Neil Armstrong', 'USA', 2),
('Yuri Gagarin', 'Russia', 1),
('Christina Koch', 'USA', 3),
('Mae Jemison', 'USA', 1),
('Valentina Tereshkova', 'Russia', 2),
('Luca Parmitano', 'Italy', 2);

-- MISSION SPACECRAFT
INSERT INTO MissionSpacecraft (MissionID, ShipID, MissionStatus)
VALUES 
(1, 1, 'Complete'),   -- Apollo 11
(2, 2, 'Ongoing'),    -- Voyager 1
(3, 3, 'Complete'),   -- JWST
(4, 6, 'Complete'),   -- Artemis I
(5, 5, 'Ongoing'),    -- ExoMars
(6, 8, 'Planned'),    -- Europa Clipper
(7, 7, 'Complete'),   -- Dragon ISS
(8, 4, 'Planned');    -- Starship Lunar

-- MISSION ASTRONAUT
INSERT INTO MissionAstronaut (MissionID, AstroID)
VALUES 
(1, 1),  -- Neil Armstrong
(2, 3),  -- Christina Koch
(3, 1),  -- Neil Armstrong
(3, 3),  -- Christina Koch
(6, 4),
(6, 6);

-- FINDINGS
INSERT INTO Finding (Significance, FindingDate, Notes)
VALUES 
('High', '1979-01-01', 'Discovered edge of heliosphere via Voyager I'),
('Medium', '2021-02-18', 'Confirmed signs of ancient habitable environment on Mars'),
('Medium', '2022-11-26', 'Orion capsule successfully returned from lunar orbit'),
('High', '2014-02-26', 'Discovered 715 new planets via Kepler'),
('High', '2019-04-10', 'Captured image of a black hole by Event Horizon Telescope'),
('Medium', '2025-03-01', 'Tested long-duration life support in deep space'),
('High', '1969-07-20', 'Confirmed successful manned landing on the Moon.'),
('High', '1990-08-25', 'Captured image of the Pale Blue Dot from Voyager 1.'),
('High', '2022-07-12', 'First deep field image from JWST revealing early galaxies.'),
('Medium', '2023-11-21', 'Detected possible organics on Mars from ExoMars instruments.'),
('Medium', '2027-05-15', 'Planned subsurface scan of Europa’s ice crust.'),
('Medium', '2021-12-06', 'Successful lunar flyby by Artemis I.');

INSERT INTO StarSystemMissions (SystemID, MissionID, StartDate, EndDate)
VALUES
(1, 1, '2029-06-01', '2030-05-12'),
(2, 8, '2021-12-25', '2022-02-01'),
(3, 7, '1969-07-16', '1969-07-24'),
(4, 4, '2030-01-12', '2031-03-12'),
(5, 6, '2033-04-20', NULL),
(6, 2, '2020-07-30', '2021-02-18'),
(8, 11, '2023-08-05', '2023-08-09'),
(12, 5, '2035-01-10', NULL),
(19, 10, '2032-11-20', NULL),
(21, 9, '2041-02-10', NULL),
(28, 12, '2046-01-05', NULL);

-- MISSION FINDING
INSERT INTO MissionFinding (MissionID, FindingID)
VALUES 
(1, 1),  -- Apollo 11 Moon landing
(2, 2),  -- Voyager Pale Blue Dot
(3, 3),  -- JWST deep field
(4, 6),  -- Artemis lunar flyby
(5, 4),  -- ExoMars organic detection
(6, 5);  -- Europa Clipper planned scan

INSERT INTO SpacecraftAstronaut (ShipID, AstroID) VALUES
(1, 5),  -- Valentina Tereshkova on Apollo 11
(1, 6),  -- Chris Hadfield on Apollo 11
(2, 1),  -- Neil Armstrong on Orion I
(3, 4),  -- Neil Armstrong on Starship Alpha
(3, 2),  -- Buzz Aldrin on Starship Alpha
(3, 3);  -- Sally Ride on Starship Alpha

Select *
FROM Planet;

SELECT P.PlanetID, P.PlanetName, P.PlanetType, P.Mass, P.NumMoons, P.Eccentricity, P.Inclination, S.StarID
FROM Planet P
         JOIN Orbits O ON P.PlanetID = O.PlanetID
         JOIN Star S ON S.StarID = O.StarID
WHERE P.PlanetID = 5;

SELECT P.PlanetID, P.PlanetName, P.PlanetType, P.Mass, P.NumMoons, P.Eccentricity, P.Inclination, S.StarID
FROM Planet P
         LEFT JOIN Orbits O ON P.PlanetID = O.PlanetID
         LEFT JOIN Star S ON S.StarID = O.StarID