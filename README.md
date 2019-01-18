# custom-django-middleware

### A custom django middleware for token based authentication

=========================

This project implements token based authentication for django applications and API's. 
It makes use of a custom middleware to check a token in each user request. If the token is present in the 
auhorization header of the request then it is matched against db and if it is valid then the user is permitted access.
Also each token has a validity of 30 minutes and after that it is revoked.

**working**
-------------------------------
