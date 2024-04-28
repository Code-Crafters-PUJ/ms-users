# msadmin-users

To run the microservice, you need to have the .env file created.

To do that:
1. Copy the example.env file and rename it to .env.
2. Then complete the environment variables with your own credentials.

3. To run the docker container, run the following command:
```bash
docker-compose up --build
```
4. To install the dependencies, run the following command, this proyect uses python > 3.10:
```bash
pip install -r requirements.txt
```
5. To create the database, run the following command:
```bash
python manage.py migrate
```
6. To run the microservice, run the following command:
```bash
python manage.py runserver
```
7. To run the tests, run the following command:
```bash
python manage.py test
```



