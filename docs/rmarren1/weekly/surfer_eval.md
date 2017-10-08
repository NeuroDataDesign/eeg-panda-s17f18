# Tech eval of PySurfer
* site: https://pysurfer.github.io/
* github: https://github.com/nipy/PySurfer

### Data input format
* To work correctly, PySurfer needs to be linked to a "FreeSurfer subjects directory", this is a directory of files formatted to be recognized by the FreeSurfer software package.
* Freesurfer "creates its own file formats for storing and manipulating volumetric, surface and transform data"
* The example plots on the PySurfer website are not reproducible given the data in the repository. E.g., while attempting to follow the [example](https://pysurfer.github.io/auto_examples/plot_basics.html#sphx-glr-auto-examples-plot-basics-py)
using the [data](https://github.com/nipy/PySurfer/tree/master/examples/example_data)
the following problem arises:
![](https://user-images.githubusercontent.com/10272301/31318351-af5ae6ce-ac1e-11e7-9ec5-4352af163356.png)
* There is hope: some [data from FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/Data).
  * With this new data, the software does not crash, but no plot is produced (gray box)
  ![](https://user-images.githubusercontent.com/10272301/31318494-c4d08d12-ac21-11e7-8c6c-f6d21786c764.png)
* When running in a normal python shell however, the code works fine
* Left an [issue](https://github.com/nipy/PySurfer/issues/190#issuecomment-335019610) to let the PySurfer devs know of the problem
