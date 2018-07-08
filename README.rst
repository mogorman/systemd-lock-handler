systemd-lock-handler
====================

Logind (part of systemd) can be configured to emit events on in response to the
lid being closed, sleeping, the power button being pressed, etc.

These events though, are simple D-Bus events, and don't actually run anything.
You need some form of wrapper to listen to these events, and run you screen
lockers, etc.

That's where this app comes in.  This simple app changes the interface
presented: it handles the ``lock`` and ``sleep`` events, and starts the
``lock.target`` ``sleep.target`` systemd targets respectively.

Note that systemd already have a ``sleep.target``, however, that's a
system-level target, and your user-level units can't rely on it. The one
included in this package does not conflict, but rather compliments that one.

Installation
------------

* Download the latest release_.
* ``tar xf v1.0.0``
* ``cd systemd-lock-handler-1.0.0/``
* ``sudo make install``

.. _release: https://github.com/WhyNotHugo/systemd-lock-handler/releases

Usage
-----

You should service files for anything you intend to intend to run on lock. For
example, ``enabling`` this service file would run ``slock``::

    [Unit]
    Description=A simple X screen locker
    Requisite=xorg.target

    [Service]
    ExecStart=/usr/bin/slock
    ExecStopPost=/usr/bin/systemctl --user start unlock.target

    [Install]
    WantedBy=lock.target

Keep in mind that, for this to work a few steps need to be taken:

Steps if you'll be using ``lock.target``
----------------------------------------

* Enable this service
  ``systemctl --user enable -- nowsystemd-lock-handler.service``.
* Edit ``/etc/systemd/logind.conf`` and set ``HandleLidSwitch=lock``. By
  default, logind has the insane behaviour of suspending on lid close. This
  makes it merely emit a lock event.

Steps if you'll be using ``sleep.target``
-----------------------------------------

* Enable this service
  ``systemctl --user enable -- nowsystemd-lock-handler.service``.

LICENCE
-------

systemd-lock-handler is licensed under the ISC licence. See LICENCE for details.
