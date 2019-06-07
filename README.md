banktrue
================

Python 3.7.3

Install packages:  pip install -r requirements.txt


Create user
================

/customers/create/

Params:

name
email
taxid
city
cellphone

Response:

{
    "name": "Alonso de Assis",
    "email": "alonsobeta@gmail.com",
    "taxid": "00224555",
    "cellphone": "34991073655",
    "city": "Patos de mina",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0YXhpZCI6IjAxNTI5MTY0NjY1In0.rARotlt3_I8b5mARau9-FIetMVLtZ0uL-vsGezsu3sg"
}

Token will be used to authenticated


Create contract
================

POST
/contract/create/

Params:

token
interest_rate
installment_number
bank
amount

response:

{
    "customer": "9ed42336-eb96-4dc4-aafe-ced36286b4b5",
    "amount": "100.00",
    "amount_due": "110.00",
    "interest_rate": "10.00",
    "installment_number": 10,
    "ip_address": "127.0.0.1",
    "bank": "Brasil"
}

Detail contract
================

GET
contracts/<uuid>?token=<mytoken>

response:

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
        }...
    
    ]
}


Pay
================

POST
/contracts/payment/

token
contract_id
id
amount_due
late_fee


response:

{
    "payment_date": "2019-06-07T14:29:15.908768",
    "due_date": "2019-11-07",
    "number": 5,
    "amount": "11.00",
    "amount_due": "11.00",
    "late_fee": "5.00"
}