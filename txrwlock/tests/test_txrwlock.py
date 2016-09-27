#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from twisted.internet import base
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import task
from twisted.trial.unittest import TestCase

from txrwlock.deferred_readers_writer_lock import DeferredReadersWriterLock


logger = logging.getLogger(__name__)


def sleep(numSec):
    return task.deferLater(reactor, numSec, lambda: None)


class ReadersWriterDeferredLockTestCase(TestCase):

    @defer.inlineCallbacks
    def testSimpleReads(self):
        lock = DeferredReadersWriterLock()
        yield lock.readerAcquire()
        yield lock.readerAcquire()
        self.assertFalse(lock.isWriting)
        yield lock.readerRelease()
        yield lock.readerRelease()

    @defer.inlineCallbacks
    def testSimpleWrites(self):
        lock = DeferredReadersWriterLock()
        self.assertFalse(lock.isWriting)
        yield lock.writerAcquire()
        self.assertTrue(lock.isWriting)
        yield lock.writerRelease()
        self.assertFalse(lock.isWriting)

    # @TxTestCase.verboseLogging()
    @defer.inlineCallbacks
    def testWrites(self):
        # Set debug to True to get full traceback of unclean deferred
        self.patch(base.DelayedCall, "debug", False)
        lock = DeferredReadersWriterLock()
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

        yield defer.gatherResults([
            read(0.1, 0.1, 10),
            read(0.1, 0.1, 10),
            write(0.15, 0.1, 15),
            write(0.17, 0.1, 20),  # should block until end of previous write
            read(0.2, 0, [15, 20]),  # '15' if read unlocked before write, else 20
            read(0.26, 0, 20),  # Should be blocked and return result of the second write
            read(0.30, 0, 20),  # Should not be blocked
        ])
        logger.debug("=== TEST FINISHED ===")
