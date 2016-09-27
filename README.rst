===============================
txrwlock
===============================
.. image:: https://travis-ci.org/Stibbons/txrwlock.svg?branch=master
    :target: https://travis-ci.org/Stibbons/txrwlock
.. image:: https://readthedocs.org/projects/txrwlock/badge/?version=latest
    :target: http://txrwlock.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://coveralls.io/repos/github/Stibbons/txrwlock/badge.svg
    :target: https://coveralls.io/github/Stibbons/txrwlock
.. image:: https://readthedocs.org/projects/txrwlock/badge/?version=latest
    :target: http://txrwlock.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Readers/Writer Lock for Twisted

- Free software: MIT
- Documentation: http://txrwlock.readthedocs.io/en/latest/
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
- This Lock is well suited for share with more readers than writer. Write requests must be at least
  an order of magnitude less often that read requests

Usage
-----

Create a virtualenv:

.. code-block:: bash

    $ virtualenv venv
    $ # virtualenv --python=python3 venv3
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
