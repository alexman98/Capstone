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

## Local Development Setup
git clone https://github.com/<your-username>/<your-repo>.git
cd your-repo

## create & activate venv
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

## install dependencies
pip install -r requirements.txt


## Authentication Setup

1. Go to Auth0 Dashboard → Applications → APIs
2. Use casting as the API Audience
3. Define roles:

| **Role**             | **Permissions**                                                                 |
|----------------------|----------------------------------------------------------------------------------|
| Casting Assistant     | `get:actors`, `get:movies`                                                      |
| Casting Director      | All above + `post:actors`, `delete:actors`, `patch:actors`, `patch:movies`     |
| Executive Producer    | All above + `post:movies`, `delete:movies`    

4. Get tokens

Auth0 Dashboard → Applications → APIs → Casting → Test tab
Generate tokens for each role.

5. 
Create setup.sh (NOT committed):
export AUTH0_DOMAIN="<YOUR_TENANT>.us.auth0.com"
export API_AUDIENCE="casting"
export ALGORITHMS="RS256"
export DATABASE_URL="postgresql://localhost:5432/casting"
export ASSISTANT_TOKEN="<PASTE_JWT>"
export DIRECTOR_TOKEN="<PASTE_JWT>"
export PRODUCER_TOKEN="<PASTE_JWT>"
echo "Env vars loaded."

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

AUTH0_DOMAIN="ADD_YOUR_DOMAIN"
API_AUDIENCE=casting
ALGORITHMS=RS256
DATABASE_URL="ADD_DB_URL"

Manual deploy (or auto-deploy on push).

 ## API Reference

Headers:
Authorization: Bearer <JWT>
Content-Type: application/json

Endpoints:

| Method | Endpoint         | Required Permission   |
|--------|------------------|------------------------|
| GET    | `/actors`        | `get:actors`          |
| GET    | `/movies`        | `get:movies`          |
| POST   | `/actors`        | `post:actors`         |
| POST   | `/movies`        | `post:movies`         |
| PATCH  | `/actors/<id>`   | `patch:actors`        |
| PATCH  | `/movies/<id>`   | `patch:movies`        |
| DELETE | `/actors/<id>`   | `delete:actors`       |
| DELETE | `/movies/<id>`   | `delete:movies`       |

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