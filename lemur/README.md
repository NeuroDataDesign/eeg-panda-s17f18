# LEMUR

LEMUR is a tool that can assist in the aggregate and one-to-one visualization of any set of data points. While this project was designed to assist in the visualization of multi-modal neuroscience/psychology datasets, it can be used for any set of objects and similarity / dissimilarity function acting on pairs of such objects.

### Installation and Usage

redlemur can be pip installed (source can also be found at the PyPI repo [here](https://pypi.org/project/redlemur/).

```
pip3 install redlemur
```

To use the package in a Python file, simply:

```
import lemur
```

### Meaning of Different Files

- **datasets.py**: Abstraction that converts directories and files into Python objects. After, it calculates distance matrices and represents those at objects as well. 
- **metrics.py**: Different metrics that can be used in calculating distance matrices.
- **embedders.py**: Different functions that can be used to embed higher dimension data into lower dimensional spaces.
- **clustering.py**: Different clustering algorithms to be used on distance matrices.
- **plotters.py**: Variety of plotting functions to be used on raw data and distance matrices.


For more detailed documentation on specific functions, [click right here](https://neurodatadesign.github.io/lemur/pkg/).
