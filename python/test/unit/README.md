This contains unit tests. Our unit tests generally use the
isoloated_dir to put things in temporary directories (typically on
/tmp/pytest-of-smyth or similiar names). If you need to look at the
output to diagnose a problem, you can inspect the output there
(see https://docs.pytest.org/en/stable/how-to/tmp_path.html for a 
discussion of this).
