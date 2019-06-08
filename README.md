banktrue
================

Python 3.7.3

Install packages:  pip install -r requirements.txt


Create User
================

POST\
**/customers/create/**

Params:

name: string \
email: string \
taxid: string\
city: string\
cellphone: string

response example:

```javascript
{
    "name": "Alonso de Assis",
    "email": "alonsobeta@gmail.com",
    "taxid": "00224555",
    "cellphone": "34991070000",
    "city": "Patos de mina",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0YXhpZCI6IjAxNTI5MTY0NjY1In0.rARotlt3_I8b5mARau9-FIetMVLtZ0uL-vsGezsu3sg"
}
```

Obs: Token will be used to authenticated

Create Contract
================

POST\
**/contract/create/**

Params:

token: string\
interest_rate: integer\
installment_number: integer\
bank: string\
amount: string

response example:

```javascript
{
    "customer": "9ed42336-eb96-4dc4-aafe-ced36286b4b5",
    "amount": "100.00",
    "amount_due": "110.00",
    "interest_rate": "10.00",
    "installment_number": 10,
    "ip_address": "127.0.0.1",
    "bank": "Brasil"
}
```

Contract Detail
================

GET\
**contracts/<uuid>?token=mytoken**

response example:

```javascript
{
    "contract": {
        "customer": "9ed42336-eb96-4dc4-aafe-ced36286b4b5",
        "amount": "100.00",
        "amount_due": "110.00",
        "interest_rate": "10.00",
        "installment_number": 10,
        "bank": "Brasil"
    },
    "summary": {
        "amount_due": 88.0,
        "amount_pay": 22.0,
        "installmets_pay": 2
    },
    "installments": [
        {
            "payment_date": "2019-06-07T14:27:52.622440",
            "due_date": "2020-01-07",
            "number": 7,
            "amount": "11.00",
            "amount_due": "11.00",
            "late_fee": "5.00"
        }
    
    ]
}
```

Constract list
================

GET\
**/contracts/user/?token=mytoken**

response example:

```javascript
[
    {
        "customer": "9ed42336-eb96-4dc4-aafe-ced36286b4b5",
        "amount": "100.00",
        "amount_due": "110.00",
        "interest_rate": "10.00",
        "installment_number": 10,
        "bank": "Brasil"
    },
    {
        "customer": "9ed42336-eb96-4dc4-aafe-ced36286b4b5",
        "amount": "100.00",
        "amount_due": "110.00",
        "interest_rate": "10.00",
        "installment_number": 10,
        "bank": "Brasil"
    }
]
```


Installment
================

GET\
**/contracts/installments/contract_id?token=mytoken**

response example:

```javascript
[
    {
        "payment_date": null,
        "due_date": "2019-10-07",
        "number": 4,
        "amount": "11.00",
        "amount_due": null,
        "late_fee": null
    },
    {
        "payment_date": null,
        "due_date": "2020-04-07",
        "number": 10,
        "amount": "11.00",
        "amount_due": null,
        "late_fee": null
    },
]
```


Pay
================

POST\
**/contracts/payment/**

Params

token: string\
contract_id: string\
id: string\
amount_due: integer\
late_fee: integer

response example:

```javascript
{
    "payment_date": "2019-06-07T14:29:15.908768",
    "due_date": "2019-11-07",
    "number": 5,
    "amount": "11.00",
    "amount_due": "11.00",
    "late_fee": "5.00"
}
```       