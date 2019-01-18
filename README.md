# custom-django-middleware

### A custom django middleware for token based authentication

----------------------------------------------------------------

This project implements token based authentication for django applications and API's. 
It makes use of a custom middleware to check a token in each user request. If the token is present in the 
auhorization header of the request then it is matched against db and if it is valid then the user is permitted access.
Also each token has a validity of 30 minutes and after that it is revoked.

**working**
-------------------------------

###**NOTE: I am accepting random new username and password and storing it as an new user So that we need not 
to create users before hand while implementing this project.**

Initially you should login using username and password. 

+ **token** - A random token will be returned. Keep note of it.
+ **request** - Now while making any request to application you should use that token inside authorization header
+ **expiration_time** - After 30 minutes the token will be expired and you have to again login
