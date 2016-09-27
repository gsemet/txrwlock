===============================
txrwlock
===============================

Readers/Writer Lock for Twisted

- Free software: MIT
- Documentation: txrwlock.readthedocs.org/en/latest/
- Source: https://github.com/Stibbons/txrwlock

Features
--------

Twisted implementation of a  `Readers/Writer Lock
<https://en.wikipedia.org/wiki/Readers–writer_lock>`_. This synchronization primitive allows to lock
a share depending on two access roles: "reader" which only access to the data without modifying it,
and "writer" which may want to change the data in the share.

- Multiple readers can access to the data at the same time. There is no locking at all when only
  readers require access to the share
- When a write requires access to the share, it prevents any new reader request to fullfil and put
  these requests into a waiting queue. It will wait for all ongoing reads to finish
- Only one writer can act at the same time

Usage
-----

Create a virtualenv:

.. code-block:: bash

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install --upgrade pip  # Force upgrade to latest version of pip

Setup for production:

.. code-block:: bash

    $ pip install -r requirements.txt .

Setup for development and unit tests

.. code-block:: bash

    $ pip install --upgrade -r requirements.txt -r requirements-dev.txt -e .

Build source package:

.. code-block:: bash

    python setup.py sdist

Build binary package:

.. code-block:: bash

    python setup.py bdist

Build Wheel package:

.. code-block:: bash

    python setup.py bdist_wheel
