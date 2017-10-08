# Tech eval of PySurfer
* site: https://pysurfer.github.io/
* github: https://github.com/nipy/PySurfer

### Data input format
* To work correctly, PySurfer needs to be linked to a "FreeSurfer subjects directory", this is a directory of files formatted to be recognized by the FreeSurfer software package.
* Freesurfer "creates its own file formats for storing and manipulating volumetric, surface and transform data"
* The example plots on the PySurfer website are not reproducible given the data in the repository. E.g., while attempting to follow the example here: https://pysurfer.github.io/auto_examples/plot_basics.html#sphx-glr-auto-examples-plot-basics-py
using the data here: https://github.com/nipy/PySurfer/tree/master/examples/example_data
the following problem arises:
![](https://user-images.githubusercontent.com/10272301/31318351-af5ae6ce-ac1e-11e7-9ec5-4352af163356.png)
