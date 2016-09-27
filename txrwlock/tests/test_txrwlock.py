#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import sys

from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import task
from twisted.trial.unittest import TestCase

from txrwlock.txrwlock import ReadersWriterDeferredLock

logger = logging.getLogger(__name__)

if sys.version_info >= (3, 5) and hasattr(defer, "deferredCoroutine"):
    g_test_async = True
else:
    g_test_async = False


def sleep(numSec):
    return task.deferLater(reactor, numSec, lambda: None)


class ReadersWriterDeferredLockTestCase(TestCase):

    @defer.inlineCallbacks
    def testReaderLock(self):
        lock = ReadersWriterDeferredLock()
        yield lock.readerAcquire()
        yield lock.readerAcquire()
        self.assertFalse(lock.isWriting)
        self.assertTrue(lock.isReading)
        yield lock.readerRelease()
        yield lock.readerRelease()

    @defer.inlineCallbacks
    def testeWriterLock(self):
        lock = ReadersWriterDeferredLock()
        self.assertFalse(lock.isWriting)
        self.assertFalse(lock.isReading)
        yield lock.writerAcquire()
        self.assertTrue(lock.isWriting)
        self.assertFalse(lock.isReading)
        yield lock.writerRelease()
        self.assertFalse(lock.isWriting)

    # if g_test_async:
    #     @defer.deferredCoroutine
    #     async def testPy3AsyncWithReaderLock(self):
    #         lock = ReadersWriterDeferredLock()
    #         async with lock.readerAcquire():
    #             self.assertTrue(lock.isReading)
    #         self.assertFalse(lock.isReading)

    @defer.inlineCallbacks
    def testeWriterBlocksReaders(self):
        lock = ReadersWriterDeferredLock()
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
