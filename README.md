# Petition API

A simple API for creating, reading, signing, and resigning petitions, secured with JWT authentication and containerized with Docker. Includes filter functionality for easier query management.

## Features:
1. **CRUD Operations**: Create, Read, Update, Delete petitions
2. **Petition Signing**: Sign and Resign petitions
3. **JWT Authentication**: Secured endpoints requiring JWT tokens
4. **Docker**: Easily run the project in a containerized environment
5. **Filters**: Query petitions using filters

## How to Run the Project?

1. Clone the repository:
   ```bash
   git clone https://github.com/ilyasqn/petitionAPI
2. Navigate to the project directory:
   ```bash
   cd petitionAPI
3. Build and run the Docker image:
   ```bash
   docker-compose up --build
4. Open your browser and go to http://localhost:8000/api/.
5. (Optional) Install Postman to easily interact with the API and handle JWT tokens.
How to Check the API?
1. Create & Read Petitions
URL: http://localhost:8000/api/petitions/
Method: POST (to create) / GET (to read all)
2. User Registration & JWT Token Retrieval
URL: http://localhost:8000/api/signup/
Method: POST
Body (x-www-form-urlencoded):
Key: username
Key: password
After signing up, you will receive a JWT token.
3. Authorize Requests
In Postman, go to the Headers section and add the following:
Key: Authorization,
Value: Bearer "your access token"
4. Update & Delete Petitions
URL: http://localhost:8000/api/petitions/int:pk/
Methods: PUT (update) / PATCH (partial update) / DELETE (delete)
Body (for updating):
title (string)
description (string)
5. Sign a Petition
URL: http://localhost:8000/api/petitions/int:pk/sign/
Method: POST
6. Resign (Remove Signature) from a Petition
URL: http://localhost:8000/api/petitions/int:pk/resign/
Method: DELETE
