# NFLFastPy

This is a Python package for easily loading nflfastR play by play data.

# Installing nflfast_py

nflfast_py is available on PyPI 

    $pip install nflfast_py

nflfast_py supports Python 3.6+

# Loading Play by Play Data

    import nflfast_py

    df = nflfast_py.load_pbp_data(year=2020)