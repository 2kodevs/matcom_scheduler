# Matcom Scheduler
School project to manage and organize the exams calendar


## Heroku setup

Steps to follow:
1. Clone this repository
2. Create a new project on heroku
3. Add a remote to your heroku project
4. Push the files to heroku
5. Add env variables NAME and TOKEN to your heroku project
6. Run the heroku project

If you has heroku CLI and you are logged, simply follow this steps:

1. `git clone https://github.com/2kodevs/matcom_scheduler.git`
2. `heroku apps:create <your-heroku-project-name>`
3. `heroku git:remote -a <your-heroku-project-name>`
4. `git push heroku main:master`
5. `heroku config:set NAME=<your-heroku-project-name> TOKEN=<your-bot-token>`
6. `heroku ps:scale web=1`