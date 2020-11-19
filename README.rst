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

* After downloading or cloning the code, navigate to the base directory and run::

    make init

this command will run the necessary docker-compose commands to build and run the containers. It will also create initial migration files and seed admin user to be able to log in

* To run the migration files::

    make db-migrate

* Next step is upgrading the database::

    make db-upgrade

* (optional) Run this command to seed the database with customers, devices and groups. **Warning** this command deletes all previous data::

    make db-seed

API Documentation
-----------------

No that the service is up and running, navigate to http://localhost:5000/swagger-ui and you should see a complete documentation of the API


Monitoring
----------

Navigate to http://localhost:8888/ to see a beautiful presentation of running tasks, queues and workers

Notification API
^^^^^^^^^^^^^^^^

This endpoint might be a bit confusing. Although it accepts to parameters `group_id` and `customer_id`, it worth mentioning that if both arguments are passed the notification will be treated as a group notification and not singular

example of notification request body::

    {
        "text": "Dear @calculate_customer_name, you have a @provided_discount % promotion valid till @provided_valid_till. Activate it using this promo code: @provided_promo_code",
        "is_dynamic": true,
        "group_id": 1,
        "extra_params": [
                {
                    "key": "@provided_discount",
                    "value": "10"
                },
                {
                    "key": "@provided_valid_till",
                    "value": "14 December"
                },
                {
                    "key": "@provided_promo_code",
                    "value": "PROMO_CODE"
                }
            ]
    }


please note that text string is treated as dynamic if you passed the field is_dynamic as True. Otherwise the service will send the text as it is (only translate it if there is a translation for it)
*   tags that starts with @provided are sent with the request body itself. You can find it under extra_params parameter.
*   tags that starts with @calculate are supposed to be calculated at the service before sending the notification. Currently supported tags are:
    *   @calculate_customer_name
    *   @calculate_customer_email
    *   @calculate_customer_phone

Translation automatically happens if the text is listed in translations.py file under notifier/ directory

Linting
-------

This project code style is black, and it uses flake8 to assure the quality of the code::

    make lint

will show run the necessary command to perform lint check on the code. Hopefully it will pass


Testing
-------
To run all test suite, run this command::

    make test

