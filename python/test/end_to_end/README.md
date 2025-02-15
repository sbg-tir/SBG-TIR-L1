This contains end to end tests. These tests tend to take longer to
run, most of them are labeled with a pytest.mark.long_test. These
tests aren't run unless you include "--run-long" in the py-test, so
you'll generally want that option when running these tests.

Our unit tests generally use the isoloated_dir to put things in
temporary directories (typically on /tmp/pytest-of-smyth or similiar
names). However, we will sometimes want access to our end to end
tests, so we place this in the in the local the end_to_end_run directory.
