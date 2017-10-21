===============================
txrwlock
===============================
.. image:: https://travis-ci.org/Stibbons/txrwlock.svg?branch=master
    :target: https://travis-ci.org/Stibbons/txrwlock
.. image:: https://ci.appveyor.com/api/projects/status/gsnw64oow1mlf72e?svg=true
    :target: https://ci.appveyor.com/project/Stibbons/txrwlock
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
- Presentation: http://www.great-a-blog.co/readerswriter-lock-for-twisted/

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

An Inlinecallbacks deferred that needs "read" access to a share use the following pattern:

.. code-block:: python

    from twisted.internet import defer
    from txrwlock import TxReadersWriterLock

    ...

    class MySharedObject(object):

        def __init__(self):
            self._readWriteLock = TxReadersWriterLock()

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

Development
-----------

Please note the following magical feature of this repository:

- This package use PBR to compute automatically the version number, generate `ChangeLog` and
  `AUTHORS`.
- Deployment to Pypi is automatically made by Travis on successful tag build. Dependencies declared
  on
- `requirements.txt` declares the strict minimum of dependencies for external modules that want to
  use `txrwlock`. These dependencies are not version frozen.
- For development, unit test, style checks, you **need** to install `requirements-dev.txt` as well.
- Travis validates txrwlock on Linux and AppVeyor on Windows

Setup for development and unit tests

.. code-block:: bash

    $ make dev

Build source package, binary package and wheel:

.. code-block:: bash

    make dists

These builds automatically generate `ChangeLog` and `AUTHOR` files from the git commit history,
thanks PBR.

Execute unit test:

.. code-block:: bash

    make test

Execute coverage:

.. code-block:: bash

    make coverage
