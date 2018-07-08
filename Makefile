DESTDIR?=/
PREFIX=/usr


install:
	@install -Dm755 handler.py \
	  ${DESTDIR}${PREFIX}/bin/systemd-lock-handler
	@install -Dm644 systemd-lock-handler.service \
	  ${DESTDIR}${PREFIX}/lib/systemd/user/systemd-lock-handler.service
	@install -Dm644 lock.target \
	  ${DESTDIR}${PREFIX}/lib/systemd/user/lock.target
	@install -Dm644 unlock.target \
	  ${DESTDIR}${PREFIX}/lib/systemd/user/unlock.target
	@install -Dm644 sleep.target \
	  ${DESTDIR}${PREFIX}/lib/systemd/user/sleep.target
