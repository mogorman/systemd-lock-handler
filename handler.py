#!/usr/bin/env python2
#
# Not that this won't run on python3 until txdbus merges #47.

import logging

from twisted.internet import defer, reactor
from txdbus import client


logger = logging.getLogger(__name__)


@defer.inlineCallbacks
def onLock():
    try:
        cli = yield client.connect(reactor, 'session')

        robj = yield cli.getRemoteObject(
            'org.freedesktop.systemd1',
            '/org/freedesktop/systemd1',
        )
        yield robj.callRemote('StartUnit', 'lock.target', 'replace')

    except Exception as e:
        logger.exception('Error starting lock.target.')


@defer.inlineCallbacks
def main():

    try:
        cli = yield client.connect(reactor, 'system')

        robj = yield cli.getRemoteObject(
            'org.freedesktop.login1',
            '/org/freedesktop/login1/session/c1',
        )

        robj.notifyOnSignal('Lock', onLock)

    except Exception as e:
        logger.exception('Error listening for lock events.')


reactor.callWhenRunning(main)
reactor.run()

# vim: ft=python