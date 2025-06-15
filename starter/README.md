# Casting Agency Capstone Project

## Project motivation

As an Executive Producer for a film studio, I require a single backend service for producing movies, administering actors, and applying role-based permissions to staff members such as assistants, casting directors, and producers.
This project exhibits:

-Relational modeling with SQLAlchemy

-REST-ful CRUD endpoints (GET | POST | PATCH | DELETE)

-Auth0 JWT authentication + RBAC

-Automated test-suite with unittest

-Continuous deployment on Render

## Live URL

**https://capstone-0qdv.onrender.com**

The API requires a valid JWT in the `Authorization` header.  
See **Authentication Setup** below to obtain a token.

## Project Dependencies

- All pinned in **requirements.txt**

## 💻 Local Development

bash
# clone + enter repo
git clone https://github.com/<your-user>/<repo>.git
cd repo

# create & activate venv
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

## Authentication Setup

1. Go to Auth0 Dashboard → Applications → APIs
2. Use casting as the API Audience
3. Define roles:

Role	Permissions
Casting Assistant	get:actors, get:movies
Casting Director	All above + post:actors, delete:actors, patch:actors, patch:movies
Executive Producer	All above + post:movies, delete:movies

4. Create setup.sh (DO NOT COMMIT):

export AUTH0_DOMAIN='your-tenant.us.auth0.com'
export API_AUDIENCE='casting'
export DATABASE_URL='postgresql://localhost:5432/casting'
export ASSISTANT_TOKEN='<PASTE_TOKEN>'
export DIRECTOR_TOKEN='<PASTE_TOKEN>'
export PRODUCER_TOKEN='<PASTE_TOKEN>'

Then load with:
source setup.sh

## To run locally:

python main.py
# or production-ready
gunicorn 'main:create_app()'

Visit: http://localhost:8080

## Deploy to Render

1. Create a PostgresSQL instance in Render
2. Create a web Service 
 * Start command: gunicorn 'main:create_app()'
 * Add environment variables from setup.sh

 ## API Reference

 Headers:
 Authorization: Bearer <JWT>
Content-Type: application/json

Endpoints:

Method	Endpoint	Permission
GET	/actors	get:actors
GET	/movies	get:movies
POST	/actors	post:actors
POST	/movies	post:movies
PATCH	/actors/<id>	patch:actors
PATCH	/movies/<id>	patch:movies
DELETE	/actors/<id>	delete:actors
DELETE	/movies/<id>	delete:movies

## Error Handling:

All errors return JSON:

{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
Handled: 400, 401, 403, 404, 422, 500

## Running Test

source setup.sh
python test_app.py

* Each endpoint tested (success + error)

* RBAC tested (min 2 tests per role)