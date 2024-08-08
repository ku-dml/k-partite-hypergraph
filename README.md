# k-partite-hypergraph

This folder contains the codes to compute the maximal solutions given a file and a list of thresholds, which is used in the paper "Data mining method of single-cell omics data to evaluate a pure tissue environment effect on gene expression level" as Algorithm 1.

Here:
- hypergraph.py: implemented code for the Algorithm 1; 
- main.py: a simple example to use the code; and
- test_main.py: a testing code (`pytest test_main.py`).

To run the codes, `pandas >= 2.0.3` is required. The testing code `test_main.py` also requires `pytest >= 8.3.2`.
You can clone the whole repository, use `cd` command on the terminal to move the current directory to the repository, and then use `pip install -e .` on the terminal to install the necessary packages.
After the installation completes, you can use `pytest test_main.py` to test if the codes are successfully installed.

For the usage of the code, please check `main.py` for more details.

A sample usage:

```
python main.py ./sample_instance/celltissue.csv > ./sample_instance/test_output.txt
```

**Notice:** Every time you run the code, exactly the same set of maximal solutions is output although the ordering may differ.
This phenomenon is caused by the usage of the data structure `set()` in python.
You can fix the ordering of the solutions by fixing the random seed.
For example, when the program is run on the command line, type:

```
export PYTHONHASHSEED=42
python main.py ./sample_instance/celltissue.csv > ./sample_instance/test_output.txt
```

You can use any positive integer as a random seed, instead of 42.
