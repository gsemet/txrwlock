# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import task

from txrwlock import TxReadersWriterLock
from txrwlock import TxTestCase

logger = logging.getLogger(__name__)


def sleep(numSec):
    return task.deferLater(reactor, numSec, lambda: None)


class TxReadersWriterLockTestCase(TxTestCase):

    shared_var = 0

    @defer.inlineCallbacks
    def testReaderLock(self):
        lock = TxReadersWriterLock()
        yield lock.readerAcquire()
        yield lock.readerAcquire()
        self.assertFalse(lock.isWriting)
        self.assertTrue(lock.isReading)
        yield lock.readerRelease()
        yield lock.readerRelease()

    @defer.inlineCallbacks
    def testWriterLock(self):
        lock = TxReadersWriterLock()
        self.assertFalse(lock.isWriting)
        self.assertFalse(lock.isReading)
        yield lock.writerAcquire()
        self.assertTrue(lock.isWriting)
        self.assertFalse(lock.isReading)
        yield lock.writerRelease()
        self.assertFalse(lock.isWriting)

    @defer.inlineCallbacks
    def testWriterBlocksReaders(self):
        lock = TxReadersWriterLock()
        self.shared_var = 10

        @defer.inlineCallbacks
        def read(delay, duration, expectedVals):
            if delay:
                yield sleep(delay)
            yield lock.readerAcquire()
            if duration:
                yield sleep(duration)
            logger.debug("Reading shared_var=%r", self.shared_var)
            if isinstance(expectedVals, list):
                self.assertIn(self.shared_var, expectedVals)
            else:
                self.assertEqual(expectedVals, self.shared_var)
            yield lock.readerRelease()

        @defer.inlineCallbacks
        def write(delay, duration, newVal):
            if delay:
                yield sleep(delay)
            yield lock.writerAcquire()
            if duration:
                yield sleep(duration)
            logger.debug("Writing shared_var=%r", self.shared_var)
            self.shared_var = newVal
            yield lock.writerRelease()

        yield defer.gatherResults(
            [
                read(0.1, 0.1, 10),
                read(0.1, 0.1, 10),
                write(0.15, 0.1, 15),
                write(0.17, 0.1, 20),  # should block until end of previous write
                read(0.2, 0, [15, 20]),  # '15' if read unlocked before write, else 20
                read(0.26, 0, 20),  # Should be blocked and return result of the second write
                read(0.30, 0, 20),  # Should not be blocked
            ]
        )
        logger.debug("=== TEST FINISHED ===")

    @defer.inlineCallbacks
    def testReaderFailure(self):
        lock = TxReadersWriterLock()

        @defer.inlineCallbacks
        def raiseAfterReadAcquire():
            try:
                yield lock.readerAcquire()

                raise Exception("Any exception")
            finally:
                yield lock.readerRelease()

        yield self.assertInlineCbRaises(Exception, raiseAfterReadAcquire)
        self.assertFalse(lock.isReading)
