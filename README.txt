Name: Maria O' Flynn
Student Number: 124423752

Name: Anastasija Smentanina
Student Number: 119389906

Group Number: 22

Github link: https://github.com/MOFlynn1233/IS2209_Assignment

Live Website: https://is2209-assignment.onrender.com

Setup:
1. Clone the repository: `git clone <github_url>`
2. Activate using either: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
3. Install the dependencies: `pip install -r requirements.txt`

Environment variables can be found in .env

To run the system:
- Locally: `python app.py`

Endpoints:
/ : Our main HTML homepage which shows the latset fun fact
/new-fact : This fetches a new fact, stores it in the Database, and redirects you to /
/health : Health check of both the database and the API

Demo Steps:
1. Run `python app.py`
2. You should see a fun fact
3. Click the "get another fact" button to fetch a new fact from the API and store it in the database
4. Visit /health to verify the dependencies are up and runningcan y