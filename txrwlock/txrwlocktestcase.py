# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from twisted.internet import defer
from twisted.trial.unittest import TestCase


__all__ = ['TxRWLockTestCase']


class TxRWLockTestCase(TestCase):
    '''
    Unit test helper class for Twisted. Provides useful methods to test exception cases, such as
    `assertRaisesWithMessage` and `assertInlineCallbacksRaisesWithMessage` in addition to
    `twisted.trial.unittest.TestCase`.
    '''
    def _handleExceptionMessageComparison(self, err, expectedMessage):
        if hasattr(err, "message"):
            # If the exception has a "message" member, use it directly, since the default case,
            # convert to str, will add unnecessary escape character arround ''
            # Example:
            #    >>> e = KeyError("invalid message: 'a string with a \"'")
            #    >>> print e
            #    'invalid message: \'a string with a "\''
            #    >>> print str(e)
            #    'invalid message: \'a string with a "\''
            #    >>> print e.message
            #    invalid message: 'a string with a "'
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
            self._handleExceptionMessageComparison(err, expectedMessage)
            return
        raise Exception("%s not raised" % (exceptionClass,))

    @defer.inlineCallbacks
    def assertInlineCallbacksRaisesWithMessage(self, exceptionClass, expectedMessage,
                                               inlineCallbacksFunc, *args, **kw):
        '''
        Assert a given inlineCallbacks decorated method raises with a given message.

        This replaces assertRaisesWithMessage for inlineCallbacks.

        Note: this method is an inlineCallbacks and need to be yielded.
        '''
        try:
            yield inlineCallbacksFunc(*args, **kw)
        except exceptionClass as err:
            self._handleExceptionMessageComparison(err, expectedMessage)
            return
        raise Exception("%s not raised" % (exceptionClass,))

    @defer.inlineCallbacks
    def assertInlineCallbacksRaises(self, exceptionClass, inlineCallbacksFunc, *args, **kw):
        '''
        Assert a given inlineCallbacks decorated method raises.

        This replaces assertRaisesWithMessage for inlineCallbacks.

        Note: this method is an inlineCallbacks and need to be yielded.
        '''
        try:
            yield inlineCallbacksFunc(*args, **kw)
        except exceptionClass:
            return
        raise Exception("{} not raised".format(exceptionClass))
