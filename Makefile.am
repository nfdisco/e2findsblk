SUBDIRS = src
uninstall-hook:
	if test -d $(DESTDIR)$(pkgpythondir); then \
	  find $(DESTDIR)$(pkgpythondir) -depth -type d -exec rmdir {} \; ; \
	fi

