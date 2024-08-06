import pytest
from main import main

@pytest.mark.parametrize(("csv_filename", "expected"),
    [
        ("./sample_instance/celltissue.csv",  29),
    ]
)

def test_main(csv_filename, expected):
    assert len(main(csv_filename)) == expected