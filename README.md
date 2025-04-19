# 📝 [QRKot](https://github.com/kopf8/cat_charity_fund)

<img src="https://pictures.s3.yandex.net/resources/sprint2_picture1_1672399951.png" width="500" alt="QRKot">

### Contents:

1. [Project tech stack](#project-tech-stack)
2. [Description](#project-description)
3. [Project deployment](#project-deployment)
4. [Available endpoints](#available-endpoints)
5. [Project created by](#project-created-by)
<br><hr>

## Project tech stack:
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
- ![SQLAlchemy](https://img.shields.io/badge/SQLALCHEMY-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white&logoSize=auto)
- ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
- ![GoogleCloudAPI](https://img.shields.io/badge/googlecloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)

<br><hr>
## Project description:
QRKot is an application for the Cat Charity Fund which supports cats.
The foundation collects donations for various targeted projects: for medical care of tailed cats in need, for the establishment of a cat colony in the basement, for food for neglected cats — for any purposes related to the support of the feline population.

## Project deployment:
Fork this repository into your GitHub profile.
Then clone your repository to your local machine via SSH:
```bash
git clone git@github.com:your_github_username/your_repository_name.git
```
Then switch to project directory:
```bash
cd cat_charity_fund
```
Then create & activate a virtual environment, upgrade pip and install project requirements:
```bash
python -m venv .venv
source .venv/Scripts/activate #for Windows users
source .venv/bin/activate #for Linux users
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Create .env file in project directory: 
```bash
touch .env
```
This file must contain the following data: 
```
APP_TITLE
APP_DESCRIPTION
DATABASE_URL
SECRET
FIRST_SUPERUSER_EMAIL
FIRST_SUPERUSER_PASSWORD
```
...and also credentials for your key & service account to access Google Drive & Google Spreadsheet.
Hint - There's a sample file _**.env.example**_ which can be used as a draft.

Create & update database by performing the following steps:
1. Make sure you have your virtual environment activated, then create & apply Alembic migrations:
```bash
alembic revision --autogenerate -m 'Migration name'
alembic upgrade head
```
2. Run the server:
```bash
uvicorn app.main:app
```
Project will be available at http://127.0.0.1:8000/

## Available endpoints

Available endpoints:
- Register & authenticate:
    - **/auth/register** - user register
    - **/auth/jwt/login** - user login (getting JWT-token)
    - **/auth/jwt/logout** - user logout (reset JWT-token)
- Users:
    - **/users/me** - get/change details of authenticated user
    - **/users/{id}** - get/change user details via user id
- Charity projects:
    - **/charity_project/** - get list of charity projects / create new charity project
    - **/charity_project/{project_id}** - change/delete existing charity project via project id
- Donations:
    - **/donation/** - get list of all donations / create new donation
    - **/donation/my** - get list of all donations done by authenticated user
- Google report:
  - **/google/** - get Google Spreadsheet report on all closed projects and the timing of their investments.

After you run the server, project specification will be available at the following endpoints: [Swagger](http://127.0.0.1:8000/docs), [ReDoc](http://127.0.0.1:8000/redoc)

All API requests were tested in [Postman](https://www.postman.com/)

## Project created by:
### [✍️ Maria Kirsanova](https://github.com/kopf8)