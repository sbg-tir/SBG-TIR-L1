# Just some basic command collected together, so I don't need to
# remember these

# We generally want to install in editable mode, so make default
install:
	pip install -e .

# Without editable mode
install2:
	pip install .

# ------------------------------------------------------------------
# See notes in README_developer.md about the
# use of linters and type checkers.
#
# It is *not* considered an error to fail these, however the output of
# the linter and type checker can useful. We try to get all the errors
# fixed just to reduce the noise in the output. You can also often
# just silence errors for things that aren't worth fixing. We aren't
# required to make the linter or type checker happy - just to write
# python code that works. But it is mildly useful to have everything
# cleanly passing so we can see the occasional real thing that the
# linter or type checker finds.
#
# Also it isn't a requirement to match the format that ruff or other
# formater want. But it is pretty easy just to run the tools to get
# constistent code, so we tend to do that.
# ------------------------------------------------------------------

lint:
	ruff check sbg_tir_l1 bin test

format:
	ruff format sbg_tir_l1 bin test

# Note that PYTHONPATH is required, at least as of pip 24.3.1. The py.typed file needed to
# tell mypy that our modules have types doesn't get translated through using
# editable mode of pip. This is an issue going back at least a few years that hasn't
# been addressed - see https://github.com/python/mypy/issues/13392. We work around this
# just by giving a explicit path to our source code skipping going through the installed
# version. This is only for type checking, all our other tests/check use the pip installed
# version.
mypy:
	PYTHONPATH=$(PWD) mypy sbg_tir_l1

check:
	pytest -n 10 test

