To successfully run the app, follow these steps:

1. Extract the file (Do not extract file into a new folder)

2. Open CMD and navigate to the "CRMS" outer folder

3. Activate the virtual environment with;
python .venv\Scripts\activate_this.py

4. If you were not able to do step three, then create a new environment with;

virtualenv .venv
python .venv\Scripts\activate_this.py

5. If you created a new environment, type in;
pip install django daphne channels

6. Finally, type in;
python manage.py runserver