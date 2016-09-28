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
.. image:: https://badge.fury.io/py/txrwlock.svg
    :target: https://pypi.python.org/pypi/txrwlock/
    :alt: Pypi package
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: ./LICENSE
    :alt: MIT licensed

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

This implementation brings this mechanism to the Twisted's deferred. Please note they are
independent with other multithreading RW lock.

For example, a data structure is shared by a different deferreds, triggered on different contexts.
Obviously, only one deferred can be writing to the data structure at a time. If more than one was
writing, then they could potentially overwrite each other's data. To prevent this from happening,
the writing deferred obtain a "writer" lock in an exclusive manner, meaning that it and only it  has
access to the data structure. Note that the exclusivity of the access is controlled strictly by
voluntary means. The opposite occurs with readers; since reading a data area is a non-destructive
operation, any number of concurent deferred can be reading the data.

However, you should protect all parts that will read data in a coherence way. For example, the
reading deferred may be confused by reading a part of the data, getting preempted by a writing
deferred, and then, when the reading deferred "resumes", continue reading data, but from a newer
"update" of the data. A data inconsistency would then result.

Heavily inspirated `by this example <http://code.activestate.com/recipes/577803-reader-writer-lock-
with-priority-for-writers/>`_.

Usage
-----

An Inlinecallbacks deferred that needs "read" access to a share use thes following pattern:

.. code-block:: python

    @defer.inlineCallbacks
    def aReaderMethod(...):
        try:
            yield rwlocker.readerAcquire()
            # ... any treatment ...
        finally:
            yield rwlocker.readerRelease()

An Inlinecallbacks deferred that needs "write" access to a share uses the following pattern:

.. code-block:: python

    @defer.inlineCallbacks
    def aWriterMethod(...):
        try:
            yield rwlocker.writerAcquire()
            # ... any treatment ...
        finally:
            yield rwlocker.writerRelease()

Setup for production
--------------------

Just ensure requirements.txt is installed with pip. This step is not useful is you use `txrwlock`
from a distribution package or a wheel.

.. code-block:: bash

    $ pip install -r requirements.txt .

Development
-----------

Create a virtualenv:

.. code-block:: bash

    $ virtualenv venv
    $ # virtualenv --python=python3 venv3
    $ source venv/bin/activate
    $ pip install --upgrade pip  # Force upgrade to latest version of pip

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

Execute unit test:

.. code-block:: bash

    trial txrwlock

Execute coverage:

.. code-block:: bash

    trial --coverage txrwlock
