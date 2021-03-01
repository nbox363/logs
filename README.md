# Logs

It's an app that has been created as a test-task for "Graffit" company

# Install

```bash
$ git clone https://github.com/nbox363/logs.git
$ cd logs
```

Create a virtualenv and activate it:
```bash
$ python3 -m venv venv
$ . venv/bin/activate
```

Install pip packages:
```bash
$ pip install -r requirements.txt
```

# Run
you may need to stop your local postgres before starting docker 
```
sudo service postgresql stop
```
to run postgres database
```bash
docker-compose up
```

to run server
```bash
cd logs
````

to run with default date 22 february 2021
```bash
python main.py
```

to run with your date

please write the date as in the example in the genitive case 
```bash
python main.py 23 января 2020
```