# ms-users

This is the documentation of the commercial user microservice


## Installation

### Steps
- Copy the example.env file and rename it to .env
- Then complete the environment variables with your own credentials.
- To run the docker container, run the following command:
```bash
docker-compose up --build
```
- To install the dependencies, run the following command, this proyect uses python > 3.10:
```bash
pip install -r requirements.txt
```
- To create the database, run the following command:
```bash
python manage.py migrate
```
- To run the microservice, run the following command:
```bash
python manage.py runserver
```
## API Reference

#### Create a company

```http
  POST /Commertial/company/createCompany
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `No Parameters` |  |  |

Json to test

```json
{
    "businessArea":"tech",
    "employeeNumber":"22",
    "NIT":"123123123123",
    "businessName":"Tasty Wooden Hat",
    "electronicBilling":"24",
    "electronicPayroll":"123123"
}
```

#### Create root user
```http
  POST /Commertial/user/createRootUser
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `No Parameters` |  |  |

Json to test

```json
{
	"name": "prueba",
  "lastname":"prueba",
  "phone":"{{$randomPhoneNumber}}",
  "email":"{{$randomEmail}}",
  "password":"asd",
  "company_NIT":"123123123123",
  "id_card":"123123123123",
  "type_id_card":"cedula"
}
```

#### Create user
```http
  POST /Commertial/user/createUser
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `No Parameters` |  |  |

Json to test

```json
{
    "name": "prueba",
    "lastname": "prueba",
    "phone": "{{$randomPhoneNumber}}",
    "email": "{{$randomEmail}}",
    "password": "asd",
    "role": "Nomina",
    "type_id_card": "Cedula",
    "id_card": "{{$randomUUID}}",
    "businessNit": "123123123123",
    "permissions": {
        "0": {
            "module": "Ventas",
            "view": true,
            "modify": false
        },
        "1": {
            "module": "Nomina",
            "view": true,
            "modify": false
        },
        "2": {
            "module": "Facturacion",
            "view": true,
            "modify": false
        }
    }
}
```



#### Login User
```http
  POST /Commertial/user/login
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `No Parameters` |  |  |

Json to test

```json
{
    "email":"prueba@prueba.com",
    "password":"asd"
}
```

#### Get accounts by company 
```http
  GET /Commertial/user/getAccountsByCompany/<id>
```
For root account only
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `String` |**JWT** key |


#### Get account 
```http
  GET /Commertial/user/<id>
```
Only root accounts can view other profiles
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `String` |**JWT** key |


#### Update account 
```http
  PUT /Commertial/user/<id>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `String` |**JWT** key |


#### Get Company 
```http
  GET /Commertial/company/<NIT>
```
Only root accounts can view other profiles
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `String` |**JWT** key |

