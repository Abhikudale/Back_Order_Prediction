# Machine_Learning_Project
This is first machine learning project
### Requirements:-
1.Github Account
2.Heroku Account
3.VS Code GUI
4.Git CLI

Creating conda environment
'''
conda create -p venv python==3.7 -y
'''
use command prompt to use below command
conda activate venv/ or conda activate venv

pip install -r requirements.txt

git status

git add .

git remove or git restore

git commit -m "message"

git remote -v

git push origin main

git branch

Herokuemailid=cv004700@gmail.com
API Key=1c9dd245-f5a8-4b53-ab30-6e98db73ee56
Heroku-app-name=machinelearningsample

Build docker image 

docker build -t <image_name>:<tagname>

>Note:-Image name for docker must be lower case
Adding this line to check if auto deployment happens

Install ipykernel
pip install ipykernel



First, update all origin/<branch> refs to latest:

git fetch --all
Backup your current branch (e.g. master):

git branch backup-master
Jump to the latest commit on origin/master and checkout those files:

git reset --hard origin/master
