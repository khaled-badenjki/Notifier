Notifier
========

Notification service based on Flask framework

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Flask%20RESTful-ff69b4.svg
     :target: https://github.com/karec/cookiecutter-flask-restful/
     :alt: Built with Cookiecutter Flask RESTful
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


Features
--------

* Dynamic templates to auto-populate notifications with real data

* Multi languages (currently Arabic and English)

* Supports SMS and push notification

* Group notifications for marketing campaigns

* Read to integrate with any SMS or Push notification provider


Technologies Used
-----------------

* Flask as a web framework (python 3.8)

* Celery as a task queue software

* RabbitMQ as a message broker

* Redis to support Celery as a backend for results

* Docker & docker-compose for containerization

* SQLite as a memory database

* Tox, PyTest and flake8 for linting and testing

* in addition to sqlAlchemy, marshmallow and other packages


Installation
------------

* After downloading or cloning the code, navigate to the base directory and run

    $ make init

this command will run the necessary docker-compose commands to build and run the containers. It will also create
initial migration files and seed admin user to be able to log in

* To run the migration files:

    $ make db-migrate

* Next step is upgrading the databse:

    $ make db-upgrade

* (optional) Run this command to seed the database with customers, devices and groups. **Warning** this command deletes all
previous data

    $ make db-seed


Linting
-------

This project code style is black, and it uses flake8 to assure the quality of the code

    $ make lint

will show run the necessary command to perform lint check on the code. Hopefully it will pass


Testing
-------

    $ make test


