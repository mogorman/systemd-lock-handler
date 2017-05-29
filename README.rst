systemd-lock-handler
====================

Logind (part of systemd) can be configured to emit events on in response to the
lid being closed, or the power button being pressed, etc.

These events though, are simple D-Bus events, and don't actually run anything.
This wrapper changes the interface presented: it handles the ``lock`` event,
and starts the ``lock.target`` systemd target.

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

* Enable this service ``systemctl --user enable systemd-lock-handler.service``.
* Edit ``/etc/systemd/logind.conf`` and set ``HandleLidSwitch=lock``. By
  default, logind has the insane behaviour of suspending on lid close. This
  makes it merely emit a lock event.

LICENCE
-------

Todoman is licensed under the MIT licence. See LICENCE for details.
