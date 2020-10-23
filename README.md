# nflfastpy

This is a Python package for easily loading nflfastR play by play data.

# Installing nflfastpy

nflfastpy is available on PyPI 

    $pip install nflfastpy

nflfastpy supports Python 3.6+

# Loading Play by Play Data

    import nflfastpy

    df = nflfastpy.load_pbp_data(year=2020)