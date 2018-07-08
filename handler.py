#!/usr/bin/env python

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
    except Exception:
        logger.exception('Error starting lock.target.')


@defer.inlineCallbacks
def onSleep(suspended):
    try:
        cli = yield client.connect(reactor, 'session')

        robj = yield cli.getRemoteObject(
            'org.freedesktop.systemd1',
            '/org/freedesktop/systemd1',
        )
        yield robj.callRemote('StartUnit', 'sleep.target', 'replace')
    except Exception:
        logger.exception('Error starting lock.target.')


@defer.inlineCallbacks
def main():
    try:
        cli = yield client.connect(reactor, 'system')

        lock_obj = yield cli.getRemoteObject(
            'org.freedesktop.login1',
            '/org/freedesktop/login1/session/c1',
        )
        sleep_obj = yield cli.getRemoteObject(
            'org.freedesktop.login1',
            '/org/freedesktop/login1',
        )

        lock_obj.notifyOnSignal('Lock', onLock)
        sleep_obj.notifyOnSignal('PrepareForSleep', onSleep)
    except Exception:
        logger.exception('Error listening for lock events.')


reactor.callWhenRunning(main)
reactor.run()
