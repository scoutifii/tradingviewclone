# Trading View
## A scalable System that supports all Financial Symbols 
### Stocks, Forex, Crypto, Commodities, Indices, etc
- With python installed
- Run the following command to create a virtual environment
    - pip -m venv tradingview_clone
- On windows
    - cd tradingview_clone\Scripts\activate.bat
- On Unix/MacOS
    - cd tradingview_clone/bin/activate
- Run command:
    - git clone https://github.com/scoutifii/tradingviewclone/tree/master
     - to the local directory tradingview_clone\Scripts
    - Or navigate to https://github.com/scoutifii/tradingviewclone/tree/master download files
    - and extract them to the local directory tradingview_clone\Scripts
- Install requirements by running command:
    - pip install -r requirements.txt
    - Create a database using the settings in a file .env of the downloaded files from the github respository given above
- Run command:
    - py manage.py makemigrations  or python manage.py makemigrations
        - incase of any errors while running the above command, just run the next command it will migrate the database
- Run command:
    - py manage.py migrate or python manage.py migrate
- Run command:
  - py manage.py runserver or python manage.py runserver
- Go to the browser enter the address below
    - http://127.0.0.1:8000/
    - It will load the interface that has login form but click signup button to signup
    - After signup is successful it will redirect you to the dashboard page
    - on the sidebar you can access the symbols by click on any of them which will redirect to its details

