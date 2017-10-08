# Tech eval of PySurfer
* site: https://pysurfer.github.io/
* github: https://github.com/nipy/PySurfer

### Data input format
* To work correctly, PySurfer needs to be linked to a "FreeSurfer subjects directory", this is a directory of files formatted to be recognized by the FreeSurfer software package.
* Freesurfer "creates its own file formats for storing and manipulating volumetric, surface and transform data"

### Getting the PySurfer demos to work
* The example plots on the PySurfer website are not reproducible given the data in the repository. E.g., while attempting to follow the [example](https://pysurfer.github.io/auto_examples/plot_basics.html#sphx-glr-auto-examples-plot-basics-py)
using the [data](https://github.com/nipy/PySurfer/tree/master/examples/example_data)
the following problem arises:
![](https://user-images.githubusercontent.com/10272301/31318351-af5ae6ce-ac1e-11e7-9ec5-4352af163356.png)
* There is hope: some [data from FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/Data).
  * With this new data, the software does not crash, but no plot is produced (gray box)
  ![](https://user-images.githubusercontent.com/10272301/31318494-c4d08d12-ac21-11e7-8c6c-f6d21786c764.png)
* When running in a normal python shell however, the code works fine
![](https://user-images.githubusercontent.com/10272301/31318961-dd483974-ac28-11e7-83ab-8b3df549151a.png)
* Left an [issue](https://github.com/nipy/PySurfer/issues/190#issuecomment-335019610) to let the PySurfer devs know of the problem
##### Structural Images
* Color is binerized based on curvature of the surfact at a point
  * darker = sulci, lighter = gyri
  ![](https://en.wikipedia.org/wiki/Sulcus_(neuroanatomy)#/media/File:Gyrus_sulcus.png)
* ![](https://user-images.githubusercontent.com/10272301/31318963-dd4beef2-ac28-11e7-9d1e-2cec02ff3db8.png)
* ![](https://user-images.githubusercontent.com/10272301/31318962-dd4b83c2-ac28-11e7-9234-a091444e8e1b.png)
* ![](https://user-images.githubusercontent.com/10272301/31318964-dd4c1814-ac28-11e7-90f0-0beb41f2e251.png)
* Artifact on the right? ![](https://user-images.githubusercontent.com/10272301/31319201-f40a4338-ac2c-11e7-8e2c-1ba9a83ea541.png)
##### Functional Images
* To get fMRI plotting to work, need to [install FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/DownloadAndInstall)
  * 10GB installation package
