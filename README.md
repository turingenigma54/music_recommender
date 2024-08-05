# Music Recommendation System

A music recommendation system built with Django that suggests tracks based on user preferences and listening history.

## Features

- User authentication system
- Personalized music recommendations
- Playlist creation and management
- Content-based filtering for track recommendations

## Technologies Used

- Python 
- Django 
- NumPy
- Scikit-learn
- PostgreSQL 
- HTML

## Installation

1. Clone the repository:
```
git clone https://github.com/turingenigma54/spotify_recommender.git
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```
3. Install the required packages:
```
pip install -r requirements.txt
```
4. Set up the database:
```
python manage.py migrate
```
5. Import track data:
- Ensure you have the `data.csv` file containing track information in the project root.
- Run the import script:
  ```
  python manage.py import_new_tracks data.csv
  ```
This step may take some time depending on the size of your dataset.

6. Create a superuser:
```
python manage.py createsuperuser
```
7. Run the development server:
```
python manage.py runserver
```

## Usage

1. Navigate to `http://localhost:8000` in your web browser.
2. Register for a new account or log in.
3. Start exploring music and getting recommendations!