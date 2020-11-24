# Task description

```
General: LOCODE REST API
Framework: Python/Django
Dockerized application
Functionality:
    - implement command to import LOCODE database: http://www.unece.org/cefact/codesfortrade/codes_index.html
        Look for function property: https://service.unece.org/trade/locode/Service/LocodeColumn.htm#Function
        Import should parse this information from raw data
    - create open api
        - two endpoints:
            - get location by code
         - searching location by NameWoDiacritics
```

1. This project uses sqlite database
2. Database is initialized with parsed UN/LOCODES 
3. To run project using **docker-compose** navigate to project directory and run `sudo docker-compose up` and open http://127.0.0.1:8000 in browser
4. To run project using **docker** use command `docker run --rm -p 8000:8000 anc813/riseapps-test-task` and open http://127.0.0.1:8000 in browser
5. Command implemented as [django-admin command](https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/) see `locode/management/commands/import_locode_database.py`
6. Command also can be called from django admin side. Run project, navigate to the admin side (username/password: `admin`/`admin`) http://127.0.0.1:8000/admin/ and click **Reparse UN/LOCODEs** button
