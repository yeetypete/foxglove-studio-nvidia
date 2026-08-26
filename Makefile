.PHONY: install uninstall

install:
	sudo ./patch-asar.py

uninstall:
	sudo ./patch-asar.py --restore
