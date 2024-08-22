# Petition API

1) Create, Read, Delete, Sign, Resign, count petition
2) JWT Authentication
3) Docker wrap


How to run the project?
1) Clone the project: git clone https://github.com/ilyasqn/petition_api
2) Go to directory: cd petition_site
3) Type: "docker build -t petition_api ." then "docker run -d -p 8000:8000 --name petition_container petition_api"
5) Do Migrations (if its needed) "docker exec -it petition_container python manage.py migrate"
6) Go http://localhost:8000/api/ (you can see all urls for check)
7) Install Postman (easier to check with JWT tokens)

How to check API?
1) List and Details of Petitions  http://localhost:8000/api/petitions/ (GET)
2) Create User  http://localhost:8000/api/register/ (fill in "Body" "x-www-form-urlencoded" Key: username, password) and Get access token (POST)
3) Go "Headers" type in Key: "Authorization" and in Value: "Bearer your access token"
4) Create a Petition   http://localhost:8000/api/petition/create/ (fill title, description in Body) (POST)
5) Sign a Petition http://localhost:8000/api/petition/sign/<int:pk>/ (POST)
6) Resign a Petition  http://localhost:8000/api/petition/resign/<int:pk>/ (DELETE)
7) Delete a Petition  http://localhost:8000/api/petition/delete/<int:pk>/ (DELETE)