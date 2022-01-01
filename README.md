# Udaan Interview Problem on Limited Time Deal
Database configuration in udaan/udaan/settings.py

DATABASES = {

    'default': {
    
        'ENGINE': 'django.db.backends.mysql',
        
        'NAME': 'udaan',
        
        'USER': 'root',
        
        'PASSWORD': 'root',
        
        'HOST': 'localhost',
        
        'PORT': '3306',
        
    }
    
}
#

TO run server at 8000 port:

python manage.py makemigrations

python manage.py migrate 

python manage.py runserver
#

API call:



Create User: [POST]

http://127.0.0.1:8000/limitedTimeDeal/createUser

Request = {

    "name": "ABC",
    
    "email": "abc@gmail.com",
    
    "password": "password123",
    
    "isSeller": "True"   #optional True for seller 
    
}
#

Create Deal: [POST]

http://127.0.0.1:8000/limitedTimeDeal/createDeal

Request = {

    "product": "ABC",
    
    "quantity": 5,
    
    "price": 2,
    
    "user": "4a0632ca13194402a7a1f7f46469f8ea",   #seller id
    
    "end_time": 3,                                #number of hour after start of deal
    
    "start_time": "01/01/2022 17:00"
    
}
#

Update Deal: [PUT]

http://127.0.0.1:8000/limitedTimeDeal/updateDeal/<str:deal_id>/

Example: http://127.0.0.1:8000/limitedTimeDeal/updateDeal/0939b6e46e5e493099aef4924b6e491f/

Request = {

    "end_time": 5                               #increase end time by 5 hours
    
}

Request = {

    "price": 4                                  #Update price to 4
    
}
#

End Deal: [PUT]

http://127.0.0.1:8000/limitedTimeDeal/endDeal/<str:deal_id>/

Example: http://127.0.0.1:8000/limitedTimeDeal/updateDeal/0939b6e46e5e493099aef4924b6e491f/

Request = {

    "isEnd": "True"
    
}
#

Claim Deal: [POST]

http://127.0.0.1:8000/limitedTimeDeal/claimDeal/<str:deal_id>/

Example: http://127.0.0.1:8000/limitedTimeDeal/claimDeal/2cd2b6354a8c4dfe84b30795b3395b32/

Request = {

    "user": "189cb8838bb14ccab7db7666fc8f91a7"    # buyer id
    
}
#
