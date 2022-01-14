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
### how to trade with bots
- navigate to core/utils/management/commands/main.py
- see notes there
- to run
```
python manage.py main
```
### how to listen incoming event from alpace

- navigate to core/utils/management/commands/listentrade.py
- see notes there
- to run
```
python manage.py listentrade
```

## Notes
- run both main and listentrade in separate terminal
- you can go to alpaca dashboard and try cancel your order
