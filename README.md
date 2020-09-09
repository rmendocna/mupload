# mupload
An exercise to deliver a file transfer tool

# Setup
(assumes a *nix-like environment)
1. checkout the repository and set it as a virtual environment
```
    $ git clone https://github.com/rmendocna/mupload.git
    $ cd mupload
    $ python3 -mvenv .
    $ . bin/activate
```
2. Install dependencies
```
    (mupload)$ pip install -r requirements
```
3. Create a user
```
    (mupload)$ python manage.py createsuperuser
```
4. Start the development server
```
    (mupload)$ python manage.py runserver
```
And browse to http://localhost:8000

