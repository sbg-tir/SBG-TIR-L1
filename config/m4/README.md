This is a small repository with autoconf m4 macros used on a variety of 
projects. We pull this out so bug fixes etc. can more easily be used across
projects.

Normally you use git subtree to put this config/m4. So assuming this has
been added as a remote autoconf-repo you would do something like:

    git subtree pull --prefix config/m4 autoconf-repo master
	
If you make local changes that should be shared with other repository, you
can go the opposite direction with:

    git subtree push --prefix config/m4 autoconf-repo master
	
We can look at differences with upstream:

    git fetch autoconf-repo
	git diff HEAD:config/m4 autoconf-repo/master

The initial creation of the subtree in a new repository is by:

    git subtree add --prefix config/m4 autoconf-repo master

Sometimes you will get errors saying "Updates were rejected because the
tip of current branch is behind." First do a subtree pull if you haven't,
this may be real. But you might get this even if a pull says everything
is up to date. This appears to be a bug in subtree, see description at
http://stackoverflow.com/questions/13756055/git-subtree-subtree-up-to-date-but-cant-push

Can try 

    git push autoconf-repo `git subtree split --prefix config/m4 master`:master --force
	
	
