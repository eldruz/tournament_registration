Tournament Registration
==============================

Disclaimer
----------
This is very much a work in progress, and until this particular statement disappears, is not really usable by any means. The name of the app is of course temporary.


What is this about?
-------------------
This is an attempt to create a full registration application aimed for fighting games tournaments created with `Django <https://www.djangoproject.com/>`_.

Planned features are :

* Manual registration of players into tournaments
* Online registration via an online shop
* Automatic synchronisation between manual and online applicants
* Export tournaments to various tournament management applications such as `Challonge <http://challonge.com/>`_ or `TioPro <http://challonge.com/>`_


LICENSE: BSD


Getting up and running
----------------------

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv
* PostgreSQL

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements/local.txt

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

You can now run the usual Django ``runserver`` command (replace ``yourapp`` with the name of the directory containing the Django project)::

    $ python yourapp/manage.py runserver

