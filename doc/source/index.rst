Readers/Writer Lock for Twisted
===============================

.. toctree::
   :maxdepth: 2


Twisted implementation of a  `Readers/Writer Lock
<https://en.wikipedia.org/wiki/Readers–writer_lock>`_.

- License: MIT
- Source: https://github.com/Stibbons/txrwlock
- Overview: http://www.great-a-blog.co/readerswriter-lock-for-twisted/

This synchronization primitive allows to lock
a share depending on two access roles: "reader" which only access to the data without modifying it,
and "writer" which may want to change the data in the share.

RW Lock features:

- Multiple readers can access to the data at the same time. There is no locking at all when only
  readers require access to the share
- When a write requires access to the share, it prevents any new reader request to fullfil and put
  these requests into a waiting queue. It will wait for all ongoing reads to finish
- Only one writer can act at the same time
- This Lock is well suited for share with more readers than writer. Write requests must be at least
  an order of magnitude less often that read requests

This implementation brings this mechanism to the Twisted's deferred. Please note they are
independent with other multithreading RW locks.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Source Documentation
====================

Readers/Writer Deferred Lock
----------------------------

.. autoclass:: txrwlock.TxReadersWriterLock
   :members:


Readers/Writer Deferred Lock TestCase
-------------------------------------

.. autoclass:: txrwlock.TxTestCase
   :members:
