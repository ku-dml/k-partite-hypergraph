# k-partite-hypergraph

## Introduction

This folder contains the codes to compute the maximal solutions given a file and a list of thresholds, which is used in the paper "Data mining method of single-cell omics data to evaluate a pure tissue environment effect on gene expression level" as Algorithm 1.

Here:
- hypergraph.py: the implemented code for the Algorithm 1; 
- main.py: a simple example to use the code; and
- test_main.py: a testing code (`pytest test_main.py`).

## Library dependencies 
`pandas >= 2.0.3`, `pytest >= 8.3.2` (only need for the testing code).

## Installation
Please clone the whole repository to use the codes. 
To install the necessary packages for the codes, use the command `pip install -e .` on the terminal (assume that the current directory is the repository).

## Test
Use `pytest test_main.py` to test if the codes are successfully installed.

## Usage
A sample usage for the computation of maximal solutions:

```
python main.py ./sample_instance/celltissue.csv > ./sample_instance/test_output.txt
```

Please check `main.py` for more details about the usage of the codes.

> [!NOTE]
> Every time you run the code, exactly the same set of maximal solutions is output although the ordering may differ.
> This phenomenon is caused by the usage of the data structure `set()` in python.
> You can fix the ordering of the solutions by fixing the random seed.
> For example, when the program is run on the command line, type:
> 
> ```
> export PYTHONHASHSEED=42
> python main.py ./sample_instance/celltissue.csv > ./sample_instance/test_output.txt
> ```
> 
> You can use any positive integer as a random seed, instead of 42.
