# Note Taking App
## Introduction
- This is a minimalistic looking notes taking web application built using **React** for the Frontend and **Flask** for the backend. 
- This app is simple to deploy as all the services have been containerized using **Docker** so it can run on any server. 
- It also uses a fully automated **Github Actions** CI pipeline to test if the backend APIs are returning the appropriate results. 

![App frontend](./images/notes-home.png)

## Features
1) Allows basic **CRUD applications** such as Create, Update, Get, and Delete certain notes or all notes in the database
2) The database is initialized using **Postgres** and runs in a separate container which means that the **data persists** in your machine as long as the docker volumes are not pruned

![How the database looks](./images/notes-db.png)

3) Extra features have been built in the frontend such as:
a. **'Create a Funny Note'** which calls 2 external APIs and posts a joke
b. **Form validation** on the frontend and backend to handle errors better
c. **Filter** all notes by clicking on an active tag

![Filter notes by tag](./images/notes-filter.png)

4) Fully automated CI pipeline which uses **Pytest** to build and run the containers (just click the **'Actions'** tab in the GitHub repo to see under the hood 😉)
5) The backend runs production-ready code which utilizes **Gunicorn** and **Gevent** to spawn multiple workers which utilize multiprocessing to ensure app runs smoothly during high load

![Gevent workers](./images/notes-workers.png)

6) Code base is comprehensively documented with comments, docstrings, type checks, and explainations to ensure a seamless review if any feature wants to be further scrutinized

## Build and Serve
This application was built using:
- Docker v20.10.18
- Docker Compose v2.9.0

Follow the following steps to start using this application:
1. Clone this repository in your local machine: `git clone https://github.com/atrikdas1/note-taking-app.git`
2. Make sure you have the right Docker and Docker Compose versions installed, otherwise it might throw odd bugs. You don't have to install anything else since the containers will install further prerequisites automatically!
3. Run the following step from inside the project folder: `docker-compose up -d --build`
4. Wait for the containers to build and start. Once done, head over to `http://localhost:3000/` and you should be able to see the fully functioning application
