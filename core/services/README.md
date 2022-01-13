## core.services

### Testing environment for JWT-based authentication

#### Set up a virtual environment
First of all, modify `ex.env` such that the environment variables are defined properly.

Then, you can create a virtual environment for testing with pipenv by following the instructions [here](../../README.md). Alternatively, set up a virtual environment in the project root with
```
pipenv install -r installer/requirements.txt
```

After that, you can spawn a shell within the virtual environment in the project root with
```
PIPENV_DOTENV_LOCATION=ex.env pipenv shell
```
You can run `echo $DBNAME` to see if the environment variables are loaded successfully. If you find that the environment variables are not configured correctly at any time point, feel free to modify `ex.env` and run the command above to start with a newly configured virtual environment again.

#### Set up a PostgreSQL database
Set up a PostgreSQL server with an empty database and a database account configured to match the connection information defined in `ex.env`.

#### Configure Django (For testing only)
**\*DO NOT REPLICATE THE FOLLOWING CONFIGURATION IN A PRODUCTION ENVIRONMENT\***

Run the following commands in the project root to initialize Django first. Follow the prompts to create a superuser. Store the credentials for the superuser account in somewhere safe.
```
python manage.py migrate
python manage.py createsuperuser
python manage.py shell -c "from django.contrib.auth.models import User; user = User.objects.create_user('user1', password='C@3vsRdNts8R5#N')"
```

### Connectivity and authentication test
Start the webserver locally with `python manage.py runserver`. Then, execute the following command in the project root to run all unit tests.
```
pytest -s
```

You should see an output similar to the following:
```
Test session starts (platform: linux, Python 3.9.9, pytest 6.2.5, pytest-sugar 0.9.4)
cachedir: .pytest_cache
django: settings: config.settings.test.development (from ini)
rootdir: /home/loratech/proj/django-boilerplate, configfile: pytest.ini
plugins: mock-3.6.1, django-4.4.0, sugar-0.9.4
collecting ... 
 tests/api/test_jwt.py::test_connection ✓               11% █▎        
 tests/api/test_jwt.py::test_token_retrieval_failure ✓  22% ██▎       
 tests/api/test_jwt.py::test_token_retrieval_success ✓  33% ███▍      
 tests/api/test_jwt.py::test_token_refresh_failure ✓    44% ████▌     
 tests/api/test_jwt.py::test_token_refresh_success ✓    56% █████▋    
 tests/api/test_jwt.py::test_sample_api_invalid_token ✓ 67% ██████▋   
 tests/api/test_jwt.py::test_sample_api_no_token ✓      78% ███████▊  
 tests/api/test_jwt.py::test_sample_api_successful_hit ✓89% ████████▉ 
 tests/api/test_jwt.py::test_permission_denied ✓       100% ██████████

Results (0.78s):
       9 passed
```