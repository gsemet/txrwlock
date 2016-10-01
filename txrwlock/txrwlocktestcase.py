# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from twisted.internet import defer
from twisted.trial.unittest import TestCase


__all__ = ['TxRWLockTestCase']


class TxRWLockTestCase(TestCase):

    '''
    Unit test helper class for Twisted.

    Provides useful methods to test exception cases, such as `assertRaisesWithMessage` and
    `assertInlineCallbacksRaisesWithMessage` in addition to `twisted.trial.unittest.TestCase`.
    '''

    def __assertExceptionMessageIs(self, err, expectedMessage):
        if hasattr(err, "message"):
            self.assertSubstring(expectedMessage, err.message)
        else:
            self.assertSubstring(expectedMessage, str(err))

    def assertRaisesWithMessage(self, exceptionClass, expectedMessage, func, *args, **kw):
        '''
        Check if a given function call (synchronous or deferred) raised with a given message.

        Note: You cannot use an inlineCallbacks as func. Please use
        assertInlineCallbacksRaisesWithMessage.
        '''
        try:
            defer.maybeDeferred(func(*args, **kw))
        except exceptionClass as err:
            self.__assertExceptionMessageIs(err, expectedMessage)
            return
        raise Exception("{0} not raised".format(exceptionClass,))

    @defer.inlineCallbacks
    def assertInlineCbRaisesWithMsg(self, exceptionClass, expectedMessage,
                                    inlineCallbacksFunc, *args, **kw):
        '''
        Assert a given inlineCallbacks decorated method raises with a given message.

        This replaces assertRaisesWithMessage for inlineCallbacks.

        Note: this method is an inlineCallbacks and need to be yielded.
        '''
        try:
            yield inlineCallbacksFunc(*args, **kw)
        except exceptionClass as err:
            self.__assertExceptionMessageIs(err, expectedMessage)
            return
        raise Exception("{0} not raised".format(exceptionClass,))

    @defer.inlineCallbacks
    def assertInlineCbRaises(self, exceptionClass, inlineCallbacksFunc, *args, **kw):
        '''
        Assert a given inlineCallbacks decorated method raises.

        This replaces assertRaisesWithMessage for inlineCallbacks.

        Note: this method is an inlineCallbacks and need to be yielded.
        '''
        try:
            yield inlineCallbacksFunc(*args, **kw)
        except exceptionClass:
            return
        raise Exception("{0} not raised".format(exceptionClass))
