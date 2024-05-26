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
  POST /Commertial/user/register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `No Parameters` |  |  |

Json to test

```json
{
    "Account": {
        "name": "prueba",
        "lastname": "prueba",
        "phone": "{{$randomPhoneNumber}}",
        "email": "{{$randomEmail}}",
        "password": "asd",
        "id_card": "{{$randomPhoneNumber}}",
        "type_id_card": "cedula"
    },
    "Company": {
        "NIT": "{{$randomPhoneNumber}}",
        "businessArea": "Tech",
        "employeeNumber": 23,
        "name": "asdasdasd"
    },
    "Bill": {
        "suscription_id": 1,
        "initial_date": "2024-03-08",
        "final_date": "2024-08-08",
        "amount": 123.099,
        "active": 1,
        "payment_date": "2024-03-09",
        "payment_method": "Credit card",
        "plan": 1,
        "coupon": "asdferasd"
    }
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

#### Get Root Accounts 
```http
  GET /Commertial/user/getRootAccount/<Id>
```
Only root accounts can view other profiles
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `String` |**JWT** key |

