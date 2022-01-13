### If you need DB
```
docker-compose -f installer/db/postgres.yml up --build -d --force-recreate
```
### install requirement
```
pip install -r installer/requirements.txt
```

### To Use
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py createbasicuser
```
