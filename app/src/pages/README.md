# Pages Documentation

Documentation for all of the pages.

# About | 30

## Purpose

> Provides a brief introduction to the application.

* Outlines the goal of the application (to be a database app that keep tracks of galaxies, stars, star systems, and more)

## How It Works

1.  Imports necessary libraries (`streamlit`, `streamlit_extras`, `modules.nav`).
2.  Renders the sidebar navigation links using the imported `SideBarLinks()` function.
3.  Displays the main title "# About this App" using `st.write`.
4.  Uses `st.markdown` to display the descriptive text about the app's purpose, and the creators.
5. Uses `st.image` to display a cute image (`faust.png`) with the caption `This is the credits section!`.

## API Connections

* This page primarily uses [Streamlit](https://streamlit.io/) for rendering the UI components.
* It uses the custom `SideBarLinks` function from `modules.nav` for navigation.
* It uses `streamlit_extras` for potentially adding features like the app logo (`add_logo` is imported but not explicitly used in the snippet).
* No direct external API calls (like to `http://api:4000`) are made from this page.

# Student Home | 100

## Purpose

> Acts as the main landing page or dashboard for Student users.

  * Greets the student by name upon login.
  * Provides direct navigation links to the primary features available to students: Galaxy Visualization, Star System Visualization, and Constellation exploration.

## How It Works

1.  **Layout & Navigation:** Sets the page layout to wide (`st.set_page_config(layout = 'wide')`) and renders the standard sidebar links using `SideBarLinks()`.
2.  **Welcome Message:** Displays a personalized welcome message ("Welcome, \[First Name]") using an f-string and accessing the user's first name stored in the Streamlit session state (`st.session_state.first_name`).
3.  **Navigation Buttons:**
      * Presents three large, primary-styled buttons (`st.button`) using `use_container_width=True` for full width.
      * Each button corresponds to a specific student feature:
          * 'View a galaxy chart'
          * 'Star Systems in detail'
          * 'Constellations'
      * Clicking a button triggers `st.switch_page` to navigate the user to the respective page file (e.g., `pages/101_Galaxy_Visualization.py`, `pages/102_Star_System_Vis.py`, `pages/103_Constellations.py`).

## API Connections

  * Uses [Streamlit](https://streamlit.io/) for UI rendering (`st.title`, `st.write`, `st.button`), session state (`st.session_state`), and internal application navigation (`st.switch_page`).
  * Imports `SideBarLinks` from the custom `modules.nav` module for sidebar navigation.
  * No direct calls to the external `http://api:4000` are made from this page; its primary function is navigation.

# Galaxy Visualization | 101

## Purpose

> Allows users to view a list of galaxies and explore the contents (star systems, stars, planets) within a specific galaxy selected by the user.

  * Displays an initial list of galaxies based on user input.
  * Provides a search mechanism to drill down into a specific galaxy by its ID.
  * Allows users to selectively view star systems, stars, and planets associated with the searched galaxy.

## How It Works

1.  **Layout & Navigation:** Renders the standard sidebar links using `SideBarLinks()`. The page layout is likely wide by default or set elsewhere.
2.  **Initial Galaxy Display:**
      * Prompts the user for the "Amount of galaxies you would like to display:" using `st.number_input`.
      * Sends a `GET` request to `http://api:4000/galaxies` with the specified `amount` as a query parameter.
      * Displays the fetched galaxy data in an interactive table using `st.dataframe`.
3.  **Galaxy Search Form (`st.form("Galaxy Searcher")`):**
      * Allows the user to input a "GalaxyID" using `st.number_input`.
      * Provides checkboxes (`st.checkbox`) for selecting which details to view: "View Star System", "View Stars", "View Planets".
      * **Search Logic (on 'Update' button click):**
          * Checks if a `GalaxyID` was entered.
          * Verifies if the entered `GalaxyID` exists within the initially fetched `data`.
          * **If valid and 'View Star System' checked:** Fetches star systems (`GET /galaxies/{GalaxyID}/starsystems`) and displays them in a dataframe.
          * **If valid and 'View Stars' checked:** Iterates through the fetched star systems, fetches stars for each system (`GET /star_systems/{StarSysID}`), displays each star's data in a dataframe, and collects all stars found.
          * **If valid and 'View Planets' checked:** Iterates through the collected stars, fetches orbiting planets for each star (`GET /planets/orbits?star={starID}`), and displays the planet data in a dataframe.

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library and [Streamlit](https://streamlit.io/) for the UI.

### Endpoints Used on This Page:

  * `GET http://api:4000/galaxies` (with `amount` param): Fetches the initial list of galaxies.
  * `GET http://api:4000/galaxies/{GalaxyID}/starsystems`: Fetches star systems within a specific galaxy.
  * `GET http://api:4000/star_systems/{StarSysID}`: Fetches stars belonging to a specific star system.
  * `GET http://api:4000/planets/orbits` (with `star` param): Fetches planets orbiting a specific star.

# MS Engineer Home | 110

## Purpose

> This page functions as a dashboard providing a quick overview of missions and serving as a launchpad to explore more specific data related to space exploration activities managed within the application.

* The home page for engineers on the platform.
* Displays the mission overview.
* Allows for mission searching/filtering.
    * It includes a form (`st.form`) where users can input a mission name to search for specific missions. The page then interacts with the backend API (`http://api:4000/missions/...`) to fetch and display data for the matching mission(s). If the search is invalid or yields no results, it falls back to fetching a default list.
* Allows users to navigate around the platform using buttons made with (`st.button`)

## How It Works

1.  The page is configured to have a wide layout (`st.set_page_config(layout='wide')`)
2.  The page renders the sidebar using the `SideBarLinks()` function which was imported.
    * This allows the user to go to one of the following pages:
        * 'View all findings' (`pages/111_Findings.py`)
        * 'View all spacecraft' (`pages/112_All_Spacecraft.py`)
        * 'View missions in detail' (`pages/113_Mission_Detail.py`)
    * This is done using `st.switch_page`.

3.  The page displays a welcome message by fetching their first name from the Streamlit session state (`st.session_state.first_name`)
4.  The form (`st.form`) is shown, containing a text input field (`st.text_input`) called "Mission Name"
    * When the user clicks the 'Update' button (`st.form_submit_button`) within the form:
        * The script checks the text that was entered in the "Mission Name" field.
        * Upon receiving invalid input the default mission list is shown.
            * `http://api:4000/missions/objective`
        * If the input contains a valid name, it attempts to fetch missions matching that specific name via the API.
            * `http://api:4000/missions/name/{title}`
        * If the name-specific search returns no data, it falls back to fetching the default list.
        * The data retrieved from the API (expected to be in JSON format) is then rendered into an interactive table using `st.dataframe`.

## API Connections

This page uses the application's local API (`http://api:4000`) as well as [Streamlit](https://streamlit.io/) and [Requests](https://pypi.org/project/requests/).

### Endpoints Used on This Page:

* `GET http://api:4000/missions/objective`: Called when the mission name search input is empty, invalid, or when a name-specific search returns no results. It gets a default list of missions
* `GET http://api:4000/missions/name/{title}`: Called when a user submits a valid mission name in the search form. `{title}` is replaced with the user's input. It retrieves missions matching that specific name.

# Findings | 111

## Purpose

> Allows users to view, search, add, and update mission findings.

* Provides functionality to associate existing findings with specific missions.

## How It Works

1.  Sets page layout to wide and renders the sidebar links.
2.  Organizes functionality into two tabs: 'View' and 'Add'.
3.  Displays all findings initially fetched from the API in a dataframe (`st.dataframe`). This includes a form (`st.form`) for searching and updating.
    * Search
        * Users enter a number (`st.number_input`) which can represent either a Finding ID or a Mission ID.
        * Checkboxes (`st.checkbox`) determine whether to search by 'Finding ID' or 'Mission ID'.
        * On form submission ('Update' button):
            * If 'Search Finding ID' is checked and a valid number is entered, fetches details for that specific finding (`GET /findings/{title}`). Displays results.
            * If 'Search Mission ID' is checked and a valid number is entered, fetches all findings associated with that mission (`GET /missions/{title}/findings`). Displays results.
    * Update/Associate
        * If a Finding ID search was performed (`findingSearch` has data), input fields for 'Notes' (`st.text_input`) and 'Significance' (`st.text_input`) appear. If these fields are filled and the form is submitted, it attempts to update the finding via `PUT /findings/{title}/Notes/{findingNotes}` and/or `PUT /findings/{title}/Sig/{findingSig}`.
        * If a Mission ID search was performed (`missionSearch` has data), a number input 'FindingID Select' (`st.number_input`) appears. If a valid Finding ID (that exists in the main `data` but not already associated with the searched mission) is entered and the form submitted, it attempts to associate this finding with the mission via `POST /missions/{title}/findings/{findingSelect}`.
    * Success messages (`st.success`) are shown upon successful API responses (status code 200).
4.  Add
    * Contains a form (`st.form`) for adding new findings.
    * Input fields include:
        * 'Significance' (`st.selectbox`: Low, Medium, High)
        * 'FindingDate' (`st.date_input`)
        * 'Notes' (`st.text_input`)
    * On form submission ('Add' button):
        * Sends a `POST` request to `/findings` with the entered data in JSON format.
        * Displays success (`st.success`) or error (`st.error`) messages based on the API response. Handles potential request exceptions.

## API Connections

This page interacts many times with the local API (`http://api:4000`) using the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/findings`: Fetches all findings (used in View tab).
* `GET http://api:4000/findings/{findingID}`: Fetches details for a specific finding.
* `GET http://api:4000/missions/{missionID}/findings`: Fetches all findings associated with a specific mission.
* `PUT http://api:4000/findings/{findingID}/Notes/{notes}`: Updates the notes for a specific finding.
* `PUT http://api:4000/findings/{findingID}/Sig/{significance}`: Updates the significance for a specific finding.
* `POST http://api:4000/missions/{missionID}/findings/{findingID}`: Associates an existing finding with a mission.
* `POST http://api:4000/findings`: Adds a new finding record.

# All Spacecraft | 112

## Purpose

> Allows users to view astronauts and parts associated with a specific spacecraft.

* Displays a list of all spacecraft.
* Provides functionality to add new parts to a selected spacecraft.
* Offers navigation to the [Astronaut Data](#astronaut-data--114) page.

## How It Works

1.  Layout & Navigation: Sets page layout to wide and renders the sidebar links.
2.  Main Form (`st.form("aaa")`):
    * Fetches and displays all spacecraft data (`GET /spacecraft`) in a dataframe.
    * Provides a number input (`st.number_input`) for users to enter a `spacecraftID`.
    * Includes a checkbox (`st.checkbox`) labeled "Add Part".
    * Update Button (`st.form_submit_button('Update')`):
        * When clicked, if a valid `spacecraftID` is entered:
            * Verifies the entered `spacecraftID` exists in the fetched spacecraft data.
            * Fetches astronaut data for the ship (`GET /astronauts/onShip/{spacecraftID}`). Displays if found.
            * Fetches part data for the ship (`GET /spacecraft/{spacecraftID}/parts`). Displays if found.
    * Add Part Functionality:
        * If the "Add Part" checkbox is checked, additional fields appear within the form:
            * 'Part Name' (`st.text_input`)
            * 'Mass In Tons' (`st.number_input`)
            * 'Length in CM' (`st.number_input`)
            * 'Part Usage' (`st.text_input`)
            * An 'Add Part' submit button (`st.form_submit_button('Add Part')`) appears.
        * When the 'Add Part' button is clicked:
            * Checks if all required part fields are filled.
            * Sends a `POST` request to `/spacecraft/{spacecraftID}/parts` with the new part data.
            * Displays success (`st.success`) or error (`st.error`) messages based on the API response.
3.  Navigation Button:
    * An `st.button` labeled 'Astronaut Data/Info' allows navigation to the [`pages/114_Astronaut_Data.py` page](#astronaut-data--114) using `st.switch_page`.

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/spacecraft`: Fetches the list of all spacecraft.
* `GET http://api:4000/astronauts/onShip/{spacecraftID}`: Fetches astronauts associated with a specific spacecraft.
* `GET http://api:4000/spacecraft/{spacecraftID}/parts`: Fetches parts associated with a specific spacecraft.
* `POST http://api:4000/spacecraft/{spacecraftID}/parts`: Adds a new part record to a specific spacecraft.

# Mission Detail | 113

## Purpose

> Provides a detailed view of missions, including extended information and associated star systems/astronauts.

* Allows users to edit existing mission details or add entirely new missions.

## How It Works

1. Sets page layout to wide and renders sidebar links.
2. Organizes functionality into 'View' and 'Edit' tabs.
3. **View Tab:**
    * Contains a form (`st.form`).
    * Fetches and displays extended mission data (`GET /missions/extended`) in a dataframe.
    * Provides a number input (`st.number_input`) for `starSystemID`.
    * Update Button: When clicked with a valid `starSystemID` entered:
        * Verifies the `starSystemID` exists in the initial extended data.
        * Fetches details for that specific star system (`GET /starsystems/{starSystemID}`). Displays data.
        * Fetches astronauts associated with missions targeting that star system (`GET /astronauts/missions/{starSystemID}`). Displays data.
4.  **Edit Tab:**
    * Contains a form (`st.form("build-a-mission")`).
    * Fetches and displays the same extended mission data (`GET /missions/extended`) for reference.
    * Fetches all star system IDs (`GET /galaxies/starsystems`) to populate a dropdown.
    * Provides a selectbox (`st.selectbox`) to choose the mode: 'Update' or 'Add'.
    * Includes input fields for mission attributes:
        * 'ID' (`st.number_input`, primarily used for 'Update' mode)
        * 'MissionName' (`st.text_input`)
        * 'Objective' (`st.text_input`)
        * 'Agency' (`st.text_input`)
        * 'SuccessRating' (`st.selectbox`: High, Medium, Low)
        * 'System ID' (`st.selectbox`, populated with fetched IDs)
        * 'StartDate' (`st.date_input`)
        * 'EndDate' (`st.date_input`)
    * **Update Button:**
        * **If 'Update' mode is selected:**
            * Verifies the entered `ID` exists.
            * For each field that has a non-empty value provided, it sends a `PUT` request to the corresponding API endpoint to update that specific attribute (e.g., `PUT /missions/{ID}/name/{MissionName}`, `PUT /missions/{ID}/objective/{Objective}`, etc.).
        * **If 'Add' mode is selected:**
            * Checks if required fields (Name, Objective, Agency, Rating, SystemID, StartDate) are provided.
            * Sends a `POST` request to `/missions` with basic mission details.
            * If successful, retrieves the newly created `MissionID` by searching for the mission name (`GET /missions/name/{MissionName}`).
            * Sends a second `POST` request to `/missions/starsystem` to link the mission to the selected star system and dates.
            * Displays success or error messages for each step.
    * Includes a 'Refresh' button which likely re-runs the form logic based on current selections.

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/missions/extended`: Fetches detailed mission data (including star system info).
* `GET http://api:4000/starsystems/{starSystemID}`: Fetches details of a specific star system.
* `GET http://api:4000/astronauts/missions/{starSystemID}`: Fetches astronauts associated with missions to a specific star system.
* `GET http://api:4000/galaxies/starsystems`: Fetches star system data (likely used to get System IDs for the dropdown).
* `GET http://api:4000/missions/name/{MissionName}`: Fetches missions by name (used to get the ID after adding).
* `PUT http://api:4000/missions/{ID}/name/{MissionName}`: Updates mission name.
* `PUT http://api:4000/missions/{ID}/objective/{Objective}`: Updates mission objective.
* `PUT http://api:4000/missions/{ID}/agency/{Agency}`: Updates mission agency.
* `PUT http://api:4000/missions/{ID}/status/{SuccessRating}`: Updates mission success rating.
* `PUT http://api:4000/missions/{ID}/starsystem/{SystemID}`: Updates the target star system for a mission.
* `PUT http://api:4000/missions/{ID}/starsystem/startdate/{StartDate}`: Updates mission start date for a star system visit.
* `PUT http://api:4000/missions/{ID}/starsystem/enddate/{EndDate}`: Updates mission end date for a star system visit.
* `POST http://api:4000/missions`: Adds a new base mission record.
* `POST http://api:4000/missions/starsystem`: Links a mission to a star system with dates.

# Astronaut Data | 114

## Purpose

> Allows viewing the missions associated with a specific astronaut.

* Provides an interface for viewing, searching, adding, updating, and deleting astronaut records.

## How It Works

1.  Sets page layout to wide and renders sidebar links.
2.  Organizes functionality into 'View' and 'Edit' tabs.
3.  **View Tab:**
    * Contains a form (`st.form("aaa")`).
    * Fetches and displays all astronaut data (`GET /astronauts`) in a dataframe.
    * Provides a selectbox (`st.selectbox`) to choose the search method: 'Search by Name' or 'Search by ID'.
    * Displays either a text input (`st.text_input`) or number input (`st.number_input`) based on the search selection.
    * Update Button: When clicked with valid search input:
        * If searching by name, calls `GET /astronauts/name/"{input}"`.
        * If searching by ID, calls `GET /astronauts/{input}`.
        * Displays the search results in a dataframe.
        * For each astronaut found, fetches and displays their associated missions (`GET /astronauts/{ID}/missions`).
4.  **Edit Tab:**
    * Contains a form (`st.form("aaaa")`).
    * Fetches and displays all astronaut data (`GET /astronauts`) for reference.
    * Provides a selectbox (`st.selectbox`) to choose the action: 'Update', 'Add', or 'Delete'.
    * Includes input fields for astronaut attributes:
        * 'ID' (`st.number_input`, required for 'Update' and 'Delete')
        * 'Country' (`st.text_input`)
        * 'Years in Space' (`st.number_input`)
        * 'Name' (`st.text_input`)
    * **Commit Button:**
        * Verifies the entered `ID` exists if the action is 'Update' or 'Delete'.
        * **If 'Update' mode:**
            * For each attribute field (Country, YearsInSpace, Name) with a non-empty value, sends a `PUT` request to update that specific field (e.g., `PUT /astronauts/{ID}/country/{Country}`).
            * Displays success/error messages.
        * **If 'Delete' mode:**
            * Sends a `DELETE` request to `/astronauts/{ID}`.
            * Displays success/error messages.
        * **If 'Add' mode:**
            * Sends a `POST` request to `/astronauts` with the Name, Country, and YearsInSpace.
            * Displays success/error messages.
    * **Refresh Button:** Refreshes the form, potentially updating the displayed mode ('in update mode!', etc.) based on the selection box.

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/astronauts`: Fetches all astronaut records.
* `GET http://api:4000/astronauts/name/"{name}"`: Searches for astronauts by name.
* `GET http://api:4000/astronauts/{astroID}`: Fetches a specific astronaut by ID.
* `GET http://api:4000/astronauts/{astroID}/missions`: Fetches missions associated with a specific astronaut.
* `PUT http://api:4000/astronauts/{astroID}/country/{country}`: Updates an astronaut's country.
* `PUT http://api:4000/astronauts/{astroID}/yearsinspace/{years}`: Updates an astronaut's years in space.
* `PUT http://api:4000/astronauts/{astroID}/name/{name}`: Updates an astronaut's name.
* `POST http://api:4000/astronauts`: Adds a new astronaut record.
* `DELETE http://api:4000/astronauts/{astroID}`: Deletes an astronaut record.

# Scientist Home | 120

## Purpose

> Acts as the main landing page or dashboard for users identified as Scientists.

* Provides quick navigation links to various data management sections relevant to scientists (Galaxy, Star System, Star, Planet databases).

## How It Works

1.  **Layout & Navigation:** Sets the page layout to wide and renders the standard sidebar links using `SideBarLinks()`.
2.  **Welcome Message:** Displays a personalized welcome message using an f-string and accessing the user's first name stored in the Streamlit session state (`st.session_state.first_name`).
3.  **Navigation Buttons:**
    * Presents a series of large, primary-styled buttons (`st.button`) using `use_container_width=True` for full width.
    * Each button corresponds to a specific data section:
        * 'Access the galaxy database'
        * 'Access the star system database'
        * 'Access the star database'
        * 'Access the planet database'
    * Clicking a button triggers `st.switch_page` to navigate the user to the respective page file (e.g., `pages/121_Galaxy_Data.py`, `pages/122_Star_System_Data.py`, etc.).

## API Connections

* Uses [Streamlit](https://streamlit.io/) for UI rendering (`st.title`, `st.write`, `st.button`) and session state (`st.session_state`).
* Uses `st.switch_page` for internal application navigation.
* Imports `SideBarLinks` from `modules.nav`.
* No direct calls to the external `http://api:4000` are made from this page; its primary function is navigation.

# Galaxy Data | 121

## Purpose

* Provides a CRUD (Create, Read, Update, Delete) interface for managing galaxy data within the application's database.
* Allows scientists to view, search, add, edit, and delete galaxy records.

## How It Works

1.  **Layout & Navigation:** Sets page layout to wide and renders sidebar links.
2.  **Tabs:** Organizes CRUD operations into four distinct tabs: 'View', 'Add', 'Edit', 'Delete'.
3.  **View Tab:**
    * Contains a form (`st.form("lookup")`) for searching.
    * Includes a text input (`st.text_input`) for the galaxy name.
    * **Search Logic:**
        * On form submission ('Search' button):
            * Checks if the input contains invalid characters ('/' or '\') or is empty. If so, fetches all galaxies (`GET /galaxies`).
            * Otherwise, attempts to fetch the specific galaxy by name (`GET /galaxies/{galaxy}`).
            * If the specific search yields no results, it falls back to fetching all galaxies.
        * Displays the fetched data using `st.dataframe`.
4.  **Add Tab:**
    * Contains a form (`st.form("input")`) for adding new galaxies.
    * Provides text inputs for 'Galaxy Name', 'Redshift', 'Year Discovered (YYYY-MM-DD)', 'Solar Mass in Trillions', and 'Dominant Element'.
    * **Add Logic:**
        * On form submission ('Add' button):
            * Constructs a JSON payload with the entered data (using `None` for empty optional fields).
            * Sends a `POST` request to `/galaxies`.
            * Displays success (`st.success`) or error (`st.error`) messages based on the API response, including specific error details if available. Handles request exceptions.
5.  **Edit Tab:**
    * Contains a form (`st.form("replace")`) for modifying existing galaxies.
    * Requires the user to input the `Galaxy ID` to be modified (`st.text_input`).
    * Provides text inputs for all galaxy attributes (Name, Redshift, Year Discovered, Solar Mass, Dominant Element).
    * **Edit Logic:**
        * On form submission ('Modify' button):
            * Constructs a JSON payload including the `GalaxyID` and all other fields.
            * Sends a `PUT` request to `/galaxies`.
            * Checks the response:
                * If successful (status 200) and `rows_affected` > 0, shows success.
                * If successful but `rows_affected` == 0, shows a warning that nothing was updated.
                * If unsuccessful, shows an error message. Handles request exceptions.
6.  **Delete Tab:**
    * Contains a form (`st.form("delete")`).
    * Includes a warning about the consequences of deletion (cascading delete of star systems).
    * Requires the user to input the `Galaxy ID` to be deleted (`st.text_input`).
    * **Delete Logic:**
        * On form submission ('Delete' button):
            * Sends a `DELETE` request to `/galaxies` with the `GalaxyID` as a query parameter.
            * Displays success (`st.success`) if status code is 200, or a warning (`st.warning`) otherwise (implying no rows were deleted). Handles request exceptions.

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/galaxies`: Fetches all galaxy records.
* `GET http://api:4000/galaxies/{galaxyName}`: Fetches a specific galaxy by its name.
* `POST http://api:4000/galaxies`: Adds a new galaxy record.
* `PUT http://api:4000/galaxies`: Updates an existing galaxy record (requires `GalaxyID` in the JSON body).
* `DELETE http://api:4000/galaxies` (with `GalaxyID` as query param): Deletes a galaxy record.

# Star System Data | 122

## Purpose

* Provides a CRUD interface for managing star system data within the application's database.
* Allows scientists to view, search (by galaxy, system, or both), add, edit, and delete star system records.

## How It Works

1.  **Layout & Navigation:** Sets page layout to wide and renders sidebar links.
2.  **Tabs:** Organizes CRUD operations into 'View', 'Add', 'Edit', 'Delete' tabs.
3.  **View Tab:**
    * Contains a form (`st.form("lookup")`) for searching.
    * Provides text inputs for 'galaxy name/id' and 'star system name/id'.
    * **Search Logic:**
        * On form submission ('Search' button):
            * Handles invalid characters ('/' or '\') in galaxy input.
            * **Case 1: Only Star System ID entered:** If `galaxy` is empty and `star_sys` is numeric, searches by system ID (`GET /starsystems/{star_sys}`).
            * **Case 2: Nothing entered / Only invalid Galaxy:** If `galaxy` is empty or invalid, displays galaxy names (`GET /galaxies/names`).
            * **Case 3: Only Galaxy entered:** If `star_sys` is empty, searches for systems within that galaxy (`GET /galaxies/{galaxy}/starsystems`).
            * **Case 4: Both Galaxy and Star System entered:**
                * Handles invalid characters in `star_sys`.
                * If `star_sys` is numeric, searches by system ID (`GET /starsystems/{star_sys}`).
                * If `star_sys` is a name, searches within the specified galaxy (`GET /galaxies/{galaxy}/starsystems/{star_sys}`).
            * Displays results in a dataframe or shows relevant error messages. Handles request exceptions.
        * If the form hasn't been submitted, displays galaxy names (`GET /galaxies/names`).
4.  **Add Tab:**
    * Contains a form (`st.form("input")`) for adding new star systems.
    * Requires 'Star System Name' (`st.text_input`, marked with '*').
    * Provides text inputs for 'Galaxy ID', 'Dist. In Light Years', 'Star System Type', and 'Num. of Stars'.
    * **Add Logic:**
        * On form submission ('Add' button):
            * Constructs JSON payload. Uses `None` for empty `SystemName`.
            * Sends a `POST` request to `/galaxies/{galaxy_id}/starsystems`.
            * Displays success or error messages based on the API response.
5.  **Edit Tab:**
    * Contains a form (`st.form("replace")`) for modifying star systems.
    * Requires 'Star System ID' to be modified (`st.text_input`, marked with '*').
    * Provides text inputs for 'Star System Name', 'Galaxy ID', 'Dist. In Light Years', 'Star System Type', and 'Num. of Stars'.
    * **Edit Logic:**
        * On form submission ('Modify' button):
            * Constructs JSON payload including `SystemID` and other fields.
            * Sends a `PUT` request to `/galaxies/{galaxy_id}/starsystems`. (Note: The endpoint seems galaxy-specific, but the payload includes `SystemID` suggesting it might update based on `SystemID` regardless of the `{galaxy_id}` in the URL path, or the `{galaxy_id}` is used for validation/context).
            * Checks response: Shows success if rows affected > 0, warning if 0 rows affected, or error otherwise.
6.  **Delete Tab:**
    * Contains a form (`st.form("delete")`).
    * Requires 'Star System ID' to be deleted (`st.text_input`, marked with '*').
    * **Delete Logic:**
        * On form submission ('Delete' button):
            * Sends a `DELETE` request to `/starsystems/{star_sys_id}`.
            * Displays success or warning based on the response status.

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library.

### Endpoints Used on This Page:

* `GET http://api:4000/starsystems/{systemID}`: Fetches a specific star system by ID.
* `GET http://api:4000/galaxies/names`: Fetches a list of galaxy names (and likely IDs).
* `GET http://api:4000/galaxies/{galaxy}/starsystems`: Fetches star systems within a specific galaxy.
* `GET http://api:4000/galaxies/{galaxy}/starsystems/{systemName}`: Fetches a specific star system by name within a galaxy.
* `POST http://api:4000/galaxies/{galaxyID}/starsystems`: Adds a new star system to a specified galaxy.
* `PUT http://api:4000/galaxies/{galaxyID}/starsystems`: Updates an existing star system (identified by `SystemID` in the payload).
* `DELETE http://api:4000/starsystems/{systemID}`: Deletes a star system by ID.

# Star Data | 123

## Purpose

> This page provides scientists with comprehensive tools to view, search, add, update, and delete star records within the database. It also facilitates exploring the stars within a given star system and identifying planets orbiting a specific star.

* Provides a CRUD (Create, Read, Update, Delete) interface for managing star data.
* Allows searching for stars within a specific star system.
* Enables searching for planets that orbit a particular star.
* Supports adding, updating, and deleting individual star records.

## How It Works

1.  **Layout & Navigation:** Sets the page layout to wide (`st.set_page_config(layout='wide')`) and renders the standard sidebar links using `SideBarLinks()`.
2.  **Tabs:** Organizes functionality into four tabs using `st.tabs`: 'View', 'Add', 'Edit', and 'Delete'.
3.  **View Tab:**
    * Contains two separate forms for different search operations.
    * **Form 1 (Search Star System's Stars):**
        * Titled "**Search a star system's stars**".
        * Provides a text input (`st.text_input`) for the user to enter a "star system name/id".
        * On form submission via the 'Search' button (`st.form_submit_button`):
            * Validates the input for invalid characters ('/' or '\') and emptiness. Displays an error (`st.error`) if invalid.
            * If valid, sends a `GET` request to `http://api:4000/star_systems/{star_sys}` to find the star system.
            * If the star system is found (response has data), it displays the data (which includes the stars within it) in a dataframe (`st.dataframe`). If not found, it displays an error.
    * **Form 2 (Lookup Star/Planets):**
        * Titled "**Look up information on a star**".
        * Provides a text input (`st.text_input`) for the "star id".
        * Includes two separate submit buttons: 'Search star information' and 'Search planets which orbit this star'.
        * **If 'Search star information' is submitted:**
            * Validates that the star ID input is numeric. Displays an error if not.
            * If numeric, sends a `GET` request to `http://api:4000/stars/{star_id}` to fetch details about the specific star.
            * Displays the star's data in a dataframe if found; otherwise, displays an error.
        * **If 'Search planets which orbit this star' is submitted:**
            * Validates that the star ID input is numeric. Displays an error if not.
            * If numeric, sends a `GET` request to `http://api:4000/planets/orbits` with the `star` query parameter set to the entered star ID.
            * Displays the data for planets orbiting that star in a dataframe if found; otherwise, displays an error.
4.  **Add Tab:**
    * Contains a form (`st.form("input")`) for adding a new star record.
    * Titled "**Add a new star to the database**".
    * Provides text inputs (`st.text_input`) for 'Star Name', 'Star System ID', 'Constellation ID', 'Mass', 'Temperature', and 'Spectral Type'.
    * On form submission via the 'Add' button (`st.form_submit_button`):
        * Constructs a JSON payload from the input values. Handles empty string inputs for optional fields by setting the corresponding JSON value to `None`.
        * Sends a `POST` request to `http://api:4000/stars` with the JSON payload.
        * Displays a success message (`st.success`) if the status code is 200. Otherwise, displays an error message (`st.error`), attempting to extract details from the API response JSON. Includes general exception handling for request failures.
5.  **Edit Tab:**
    * Contains a form (`st.form("update")`) for updating an existing star record.
    * Titled "**Update a star**".
    * Requires "*Star ID to be modified:*" (`st.text_input`).
    * Provides text inputs (`st.text_input`) for 'Star Name', 'Star System ID', 'Constellation ID', 'Mass', 'Temperature', and 'Spectral Type' to enter the updated values.
    * On form submission via the 'Update' button (`st.form_submit_button`):
        * Constructs a JSON payload including the required `StarID` and the other provided attribute values.
        * Sends a `PUT` request to `http://api:4000/stars` with the JSON payload.
        * Checks the response: If status code is 200, it examines the JSON result's `rows_affected`. If 0, displays a warning (`st.warning`); otherwise, displays a success message (`st.success`). If the status code is not 200, displays an error message (`st.error`). Includes exception handling for request failures.
6.  **Delete Tab:**
    * Contains a form (`st.form("delete")`) for deleting a star record.
    * Titled "**Delete a star**".
    * Requires "*Star ID to be deleted:*" (`st.text_input`).
    * On form submission via the 'Delete' button (`st.form_submit_button`):
        * Sends a `DELETE` request to `http://api:4000/stars` with the `StarID` included as a query parameter (`params={"StarID": star_id}`).
        * Displays a success message (`st.success`) if the status code is 200, or a warning message (`st.warning`) if the status code is not 200 (implying no rows were deleted). Includes exception handling for request failures.

## API Connections

This page interacts with the application's local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library and [Streamlit](https://streamlit.io/) for UI.

### Endpoints Used on This Page:

* `GET http://api:4000/star_systems/{star_sys}`: Fetches data for a star system, including its stars, used for searching stars by system.
* `GET http://api:4000/stars/{star_id}`: Fetches details for a specific star by its ID.
* `GET http://api:4000/planets/orbits` (with `star` param): Searches for planets that orbit a specific star ID.
* `POST http://api:4000/stars`: Adds a new star record (requires data in the JSON body).
* `PUT http://api:4000/stars`: Updates an existing star record (requires `StarID` and updated data in the JSON body).
* `DELETE http://api:4000/stars` (with `StarID` as query param): Deletes a star record based on its ID.

# Planet Data | 124

## Purpose

> This page allows scientists to manage both planet records and their associated orbital information within the database. It provides interfaces for viewing, searching, adding, updating, and deleting planets, as well as managing the orbital relationships between planets and stars.

* Provides a CRUD (Create, Read, Update, Delete) interface for managing planet data.
* Provides a CRUD interface for managing planet orbital relationships with stars.
* Allows searching for planets by name or ID.
* Enables searching for orbital information related to a specific star.

## How It Works

1.  **Layout & Navigation:** Sets the page layout to wide (`st.set_page_config(layout='wide')`) and renders the standard sidebar links using `SideBarLinks()`.
2.  **Tabs:** Organizes functionality into three tabs using `st.tabs`: 'View Planets/Orbits', 'Modify Planets', and 'Modify Orbits'.
3.  **View Planets/Orbits Tab:**
    * Contains two separate forms for different viewing operations.
    * **Form 1 (Search Star's Orbits):**
        * Titled "**Search a star's orbits**".
        * Provides a text input (`st.text_input`) for the user to enter a "star name/id".
        * On form submission via the 'Search' button (`st.form_submit_button`):
            * Validates the input for invalid characters ('/' or '\') and emptiness. Displays an error (`st.error`) if invalid.
            * If valid, sends a `GET` request to `http://api:4000/planets/orbits` with the `star` query parameter set to the entered star name/id.
            * Displays the retrieved orbital data in a dataframe (`st.dataframe`) if found; otherwise, displays an error.
    * **Form 2 (Lookup Planet):**
        * Titled "**Lookup information on a planet**".
        * Provides a text input (`st.text_input`) for the user to enter a "planet name/id".
        * On form submission via the 'Search' button (`st.form_submit_button`):
            * Validates the input for invalid characters ('/' or '\') and emptiness. Displays an error if invalid.
            * If valid, sends a `GET` request to `http://api:4000/planets/{planet_identifier}` to fetch details about the specific planet.
            * Displays the planet's data in a dataframe if found; otherwise, displays an error.
4.  **Modify Planets Tab:**
    * Contains three separate forms within this tab for Add, Update, and Delete operations on **planet records**.
    * **Form 1 (Add Planet):**
        * Titled "**Add a new planet to the database**".
        * Provides text inputs (`st.text_input`) for 'Planet Name', 'Planet Type', 'Mass', 'Num. of Moons', 'Eccentricity', and 'Inclination'.
        * On form submission via the 'Add' button (`st.form_submit_button`):
            * Constructs a JSON payload from the input values, setting empty optional fields to `None`.
            * Sends a `POST` request to `http://api:4000/planets` with the JSON payload.
            * Displays success or error messages based on the API response and includes exception handling.
    * **Form 2 (Update Planet):**
        * Titled "**Update a planet**".
        * Requires "*Planet ID to be modified:*" (`st.text_input`).
        * Provides text inputs for other planet attributes to enter updated values.
        * On form submission via the 'Update' button (`st.form_submit_button`):
            * Constructs a JSON payload including the required `PlanetID` and other provided values.
            * Sends a `PUT` request to `http://api:4000/planets` with the JSON payload.
            * Checks the response's `rows_affected` for success ( > 0), warning (0), or displays an error for other non-200 responses. Includes exception handling.
    * **Form 3 (Delete Planet):**
        * Titled "**Delete a planet**".
        * Requires "*Planet ID to be deleted:*" (`st.text_input`).
        * On form submission via the 'Delete' button (`st.form_submit_button`):
            * Sends a `DELETE` request to `http://api:4000/planets` with the `PlanetID` included as a query parameter.
            * Displays success or warning messages based on the status code and includes exception handling.
5.  **Modify Orbits Tab:**
    * Contains three separate forms within this tab for Add, Update, and Delete operations on **planet orbital status records**.
    * **Form 1 (Add Orbit):**
        * Titled "**Add a new planet's orbital status to the database**".
        * Requires "*Planet ID:*" and "*Star ID:*" (`st.text_input`).
        * Provides text inputs for 'Orbital Period' and 'Semi-major axis'.
        * On form submission via the 'Add' button (`st.form_submit_button`):
            * Constructs a JSON payload including the required IDs and optional period/axis.
            * Sends a `POST` request to `http://api:4000/planets/orbits` with the JSON payload.
            * Displays success or error messages and includes exception handling.
    * **Form 2 (Update Orbit):**
        * Titled "**Update a planet's orbital status**".
        * Requires "*Planet ID to be modified:*" and provides text input for "Star ID:".
        * Provides text inputs for 'Orbital Period' and 'Semi-major axis' to enter updated values.
        * On form submission via the 'Update' button (`st.form_submit_button`):
            * Constructs a JSON payload including the required `PlanetID` and potentially the `StarID`, period, and axis. (Note: The update endpoint uses both PlanetID and StarID to identify the specific orbital record).
            * Sends a `PUT` request to `http://api:4000/planets/orbits` with the JSON payload.
            * Checks the response's `rows_affected` for success ( > 0), warning (0), or displays an error for other non-200 responses. Includes exception handling.
    * **Form 3 (Delete Orbit):**
        * Titled "**Delete a planet's orbital info**".
        * Requires "*Orbit's Star ID:*" and "*Orbit's Planet ID:*" (`st.text_input`) to uniquely identify the orbital record.
        * On form submission via the 'Delete' button (`st.form_submit_button`):
            * Sends a `DELETE` request to `http://api:4000/planets/orbits` with a JSON payload containing the `PlanetID` and `StarID` to specify which orbital relationship to delete.
            * Displays success or warning messages based on the status code and includes exception handling.

## API Connections

This page interacts heavily with the application's local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library and [Streamlit](https://streamlit.io/) for UI.

### Endpoints Used on This Page:

* `GET http://api:4000/planets/orbits` (with `star` param): Fetches orbital information for planets associated with a specific star (by name or ID).
* `GET http://api:4000/planets/{planet_identifier}`: Fetches details for a specific planet by its name or ID.
* `POST http://api:4000/planets`: Adds a new planet record (requires data in the JSON body).
* `PUT http://api:4000/planets`: Updates an existing planet record (requires `PlanetID` and updated data in the JSON body).
* `DELETE http://api:4000/planets` (with `PlanetID` as query param): Deletes a planet record based on its ID.
* `POST http://api:4000/planets/orbits`: Adds a new planet orbital record (requires `PlanetID`, `StarID`, and optional data in the JSON body).
* `PUT http://api:4000/planets/orbits`: Updates an existing planet orbital record (requires `PlanetID`, `StarID`, and updated data in the JSON body).
* `DELETE http://api:4000/planets/orbits` (with JSON body containing `PlanetID` and `StarID`): Deletes a specific planet orbital record.

# Astrologist Home | 130

## Purpose

> Serves as the main landing page or dashboard for users identified as Astrologists.

  * Greets the astrologist by name.
  * Provides quick navigation links to the primary features relevant to astrologists: viewing all constellation information and finding the constellation for a specific star.

## How It Works

1.  **Layout & Navigation:** Sets the page layout to wide (`st.set_page_config(layout = 'wide')`) and renders the standard sidebar links using `SideBarLinks()`.
2.  **Welcome Message:** Displays a personalized welcome message ("Welcome, \[First Name]") using `st.title` and accessing the user's first name from `st.session_state.first_name`.
3.  **Navigation Buttons:**
      * Presents two large, primary-styled buttons (`st.button`) using `use_container_width=True`.
      * Each button corresponds to a specific astrologist feature:
          * 'View all constellations and their information'
          * 'See which constellation a certain star is in'
      * Clicking a button triggers `st.switch_page` to navigate the user to the respective page file (`pages/131_Constellation_Info.py` or `pages/132_Find_Constellation.py`).

## API Connections

  * Uses [Streamlit](https://streamlit.io/) for UI rendering (`st.title`, `st.write`, `st.button`), session state (`st.session_state`), and internal application navigation (`st.switch_page`).
  * Imports `SideBarLinks` from the custom `modules.nav` module.
  * No direct calls to the external `http://api:4000` are made from this page; its primary function is navigation.

# Constellation Info | 131

## Purpose

> Displays detailed information for all constellations available in the database.

  * Fetches and presents key details for each constellation, such as abbreviation, hemisphere, brightest star, and notes.

## How It Works

1.  **Layout & Navigation:** Sets the page layout to wide (`st.set_page_config(layout='wide')`) and renders the standard sidebar links using `SideBarLinks()`.
2.  **Data Fetching:**
      * Attempts to send a `GET` request to `http://api:4000/constellation` to retrieve data for all constellations.
      * Includes basic error handling (`try...except`) for `requests.exceptions.RequestException` to catch connection issues. If an error occurs, it displays "Could not connect to API :c".
3.  **Information Display:**
      * If the data is fetched successfully:
          * Displays a main title "🌟 Information on all the constellations\!".
          * Iterates through the list of constellation objects received from the API.
          * For each `constellation`:
              * Displays the constellation name (`ConstName`) as a level 3 header (`st.write(f"### ...")`).
              * Uses `st.markdown` to present formatted information: "Also abbreviated as **\[Abbreviation]**. Located in the \[Hemisphere]ern hemisphere, and its brightest star is **\[BrightestStar]**. A fun fact: \[Notes]."

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library and [Streamlit](https://streamlit.io/) for the UI.

### Endpoints Used on This Page:

  * `GET http://api:4000/constellation`: Fetches information for all constellations.

# Find Constellation | 132

## Purpose

> Allows users (presumably Astrologists) to look up which constellation a specific star belongs to.

  * Provides a simple interface to enter a star name and retrieve its associated constellation.

## How It Works

1.  **Layout & Navigation:** Sets the page layout to wide (`st.set_page_config(layout='wide')`) and renders the standard sidebar links using `SideBarLinks()`.
2.  **Input Form (`st.form("star_lookup_form")`):**
      * Presents a text input field (`st.text_input`) prompting the user to "Enter the star name you wish to look up:".
      * Includes a submit button ("Lookup Star").
3.  **Lookup Logic (triggered by form submission):**
      * Retrieves the `star` name entered by the user.
      * Sends a `GET` request to the API endpoint `http://api:4000/constellation/star/{star}` where `{star}` is the entered name.
      * Includes error handling using `try...except` for `requests.exceptions.RequestException`:
          * Catches connection errors or bad responses (like 4xx or 5xx) using `response.raise_for_status()`. Displays an error message (`st.error`) and the exception details (`st.text`).
      * **Result Display:**
          * If the API call is successful and returns data (`if data:`):
              * Displays the result using `st.markdown`: "🌟 The star **\[star name]** is in the **\[Constellation Name]** constellation." (Accesses `data[0]['ConstName']`).
          * If the API call is successful but returns no data (`else:`):
              * Displays a warning message (`st.warning`): "No constellation found for **\[star name]**."

## API Connections

Uses the local API (`http://api:4000`) via the [Requests](https://pypi.org/project/requests/) library and [Streamlit](https://streamlit.io/) for the UI.

### Endpoints Used on This Page:

  * `GET http://api:4000/constellation/star/{starName}`: Fetches the constellation associated with a specific star name.