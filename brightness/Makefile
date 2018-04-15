all:
	if test "`whoami`" = "root" ; then echo "Got root";g++ -o /usr/bin/brightness brightness.cpp;chmod 4755 /usr/bin/brightness;else echo "You need to be root, but you're `whoami`. Try \"sudo make\"";fi
