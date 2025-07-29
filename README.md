JurisFlow is a legal case management system designed for law firms, enabling efficient task organization, client interaction, and financial oversight — all in one place. 
With a Trello-style board layout, calendar integration, and customizable activity tracking (meetings, hearings, legal deadlines), JurisFlow brings structure and clarity to legal workflows.

Features

- Kanban-style task board
- Activity types: client meetings, hearings, and legal deadlines
- Calendar view with event scheduling
- Financial dashboard for tracking revenue and client billing
- Responsive UI with Bootstrap

Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default, but adaptable)
- **Version Control:** Git + GitHub

Installation

```bash
git clone https://github.com/lauralencarr/JurisFlow.git
cd JurisFlow
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
