# -*- coding: utf-8 -*-
# Twisted implementation of the Readers/Writer Lock
# Inspirated by:
#   http://code.activestate.com/recipes/577803-reader-writer-lock-with-priority-for-writers/
# License:
#   MIT License
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from twisted.internet import defer


class _LightSwitch(object):
    '''
    An auxiliary "light switch"-like object. The first deferred turns on the "switch", the
    last one turns it off.
    '''

    def __init__(self):
        self.__cnt = 0
        self.__m = defer.DeferredLock()

    @defer.inlineCallbacks
    def acquire(self, lock):
        '''
        Acquire the lock and increase the counter
        '''
        yield self.__m.acquire()
        self.__cnt += 1
        if self.__cnt == 1:
            yield lock.acquire()
        self.__m.release()

    @defer.inlineCallbacks
    def release(self, lock):
        '''
        Release the lock and decreaser the counter
        '''
        yield self.__m.acquire()
        self.__cnt -= 1
        if self.__cnt == 0:
            lock.release()
        self.__m.release()


class ReadersWriterDeferredLock(object):

    '''
    Readers-Writer Lock for Twisted's Deferred

    Many readers can simultaneously access a share at the same time, but a writer has an exclusive
    access to this share.

    The following constraints should be met:
    1) no reader should be kept waiting if the share is currently not opened to anyone or to only
       other readers.
    2) only one writer can open the share at the same time, and when multiple writer request access,
       they will waiting for the execution of all previous writer access

    Reads and Writes are executed from within the main twisted reactor. Do **NOT** call it from
    external threads (e.g., from synchronous method execute in thread with ``deferToThread``).

    Description
    -----------

    "Readers" uses ``readerAcquire`` and ``readerRelease``.
    "Writer" uses ``writerAcquire`` and ``writerRelease``.

    Python version > 3.5 can also use `async with reader`

    A "reader" is not blocked when 2 or more 'reads' are executing.
    A "reader" is blocked when a 'writer' is executing.

    When a "write" is started, it blocks all new 'reads' and wait for the pending 'reads' to finish.
    If a new 'write" is requested, it will wait for running writes to finish as well.

    Notes:

        Please be aware than ``ReadersWriterDeferredLock.acquire*`` and
        ``ReadersWriterDeferredLock.release*`` methods are deferred, which is different from
        ``defer.DeferredLock``, where only the ``defer.DeferredLock.acquire()`` method is a
        deferred.

    Usage
    -----

    Threads that just need "read" access, use the following pattern:

    .. code-block:: python

        @defer.inlineCallbacks
        def aReaderMethod(...):
            try:
                yield rwlocker.readerAcquire()
                # ... any treatment ...
            finally:
                yield rwlocker.readerRelease()

    Threads that just need "read" access, use the following pattern:

    .. code-block:: python

        @defer.inlineCallbacks
        def aWriterMethod(...):
            try:
                yield rwlocker.writerAcquire()
                # ... any treatment ...
            finally:
                yield rwlocker.writerRelease()
    '''

    def __init__(self):
        self.__rd_swtch = _LightSwitch()
        self.__wrte_swtch = _LightSwitch()
        self.__no_rdr = defer.DeferredLock()
        self.__no_wrtr = defer.DeferredLock()
        self.__rdrs_q = defer.DeferredLock()

    @property
    def isReading(self):
        '''
        Is the lock acquired for read? (will return false if only required for writer)
        '''
        return self.__no_wrtr.locked and not self.__no_rdr.locked

    @property
    def isWriting(self):
        '''
        Is the lock acquired for write?
        '''
        return self.__no_rdr.locked

    @defer.inlineCallbacks
    def readerAcquire(self):
        """
        Acquire the lock for a Reader.

        If the lock has been acquire by only reader, this method will not block.
        If the lock has been requested by at least one writer, even if this writer is waiting for
        all ongoing readers to finish, this call will be blocked
        """

        yield self.__rdrs_q.acquire()
        yield self.__no_rdr.acquire()
        yield self.__rd_swtch.acquire(self.__no_wrtr)
        self.__no_rdr.release()
        self.__rdrs_q.release()

    @defer.inlineCallbacks
    def readerRelease(self):
        """
        Release the lock by a reader
        """
        yield self.__rd_swtch.release(self.__no_wrtr)

    @defer.inlineCallbacks
    def writerAcquire(self):
        """
        Acquire the lock for a Writer

        If at least one other reader is ongoing, this call will block any new reader request, and
        will wait for all reader to finish.

        If two writer request access to the lock, each one will wait so only one write has the lock
        at the a time.
        """

        yield self.__wrte_swtch.acquire(self.__no_rdr)
        yield self.__no_wrtr.acquire()

    @defer.inlineCallbacks
    def writerRelease(self):
        """
        Release the lock by a Writer
        """
        self.__no_wrtr.release()
        yield self.__wrte_swtch.release(self.__no_rdr)


__all__ = [ReadersWriterDeferredLock]
