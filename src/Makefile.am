e2findsblk_PYTHON = __init__.py e2findsblk.py
e2findsblkdir = $(pkgpythondir)
dist_bin_SCRIPTS = e2findsblk
CLEANFILES = $(dist_bin_SCRIPTS)
$(dist_bin_SCRIPTS): $(addsuffix .py,$(dist_bin_SCRIPTS))
	if [ -n "$(dist_bin_SCRIPTS)" ]; then \
	  for script in $(dist_bin_SCRIPTS); do \
	    printf "#!/bin/sh\npython -m e2findsblk.$$script \"\$$@\"\n" \
	      > $$script ; \
	  done ; \
	fi

