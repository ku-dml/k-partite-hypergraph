# k-partite-hypergraph

This folder contains the codes to compute the maximal solutions given a file and a list of thresholds, which is used in the paper "Data mining method of single-cell omics data to evaluate a pure tissue environment effect on gene expression level".

Here:
- hypergraph.py: implemented code for the Algorithm 1; and
- main.py: a simple example to use the code.

Please check `main.py` for more details for the usage of the code.

A sample usage:

```
python main.py ./sample_instance/celltissue.csv > ./sample_instance/test_output.txt
```

Notice: The ordering of the obtained maximal solutions may differ every time you run the code.
This phenomenon is caused by the usage of the data structure `set()` in python.
You can fix the ordering of the solutions by fixing the random seed; e.g., type `export PYTHONHASHSEED=42` first on the command lines before running the code.

