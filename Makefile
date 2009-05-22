
all: menu
menu:
	@echo "To install 'make install'"
	@echo "to uninstall 'make uninstall'"

msg:
	@echo "Dependency: mpg123, flac, oggenc, catdoc, python,  => 2.5.2 "

install: msg
	install ./scon /usr/bin/
	mkdir -p /usr/local/lib/sCon
	cp -rf ./main /usr/local/lib/sCon
	[ -e /usr/local/share/man/man1/ ] || mkdir -p /usr/local/share/man/man1/
	gzip ./man/scon.1 -c > /usr/local/share/man/man1/scon.1.gz
	[ -e /usr/local/share/man/es/man1/ ] || mkdir -p /usr/local/share/man/es/man1/
	gzip ./man/es/scon.1 -c > /usr/local/share/man/es/man1/scon.1.gz


uninstall:
	@echo "Deletting sCon"
	rm -f /usr/local/bin/scon
	rm -rf /usr/local/lib/sCon/
	rm -f /usr/local/share/man/man1/scon.1*
	rmdir --ignore-fail-on-non-empty /usr/local/share/man/man1/
	rm -f /usr/local/share/man/es/man1/scon.1*
	rmdir --ignore-fail-on-non-empty /usr/local/share/man/es/man1/
	rmdir --ignore-fail-on-non-empty /usr/local/share/man/es/
