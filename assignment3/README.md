# Instapy
## About the package
Instapy is a package created to apply grayscale and sepia filters to images, while exploring the differences between different implementations.
## Requirements
Python 3.7 or greater \
numpy \
numba \
PIL

## Install
The package is called 'instapy' \
Can be installed with:
```
pip install .
```

## How to run
### Run in terminal with
```
instapy <image> <arguments>
```
or
```
python3 -m instapy <image> <arguments>
```
Arguments include:
- `-h` for receiving help message
- `-o OUT` for saving filtered image with filename `OUT`
- `-g` for applying gray filter
- `-se` for applying sepia filter
- `-sc SCALE` for scaling image down by a factor `SCALE`
- `-i {python, numpy, numba}` for choosing implementation
- `-r` for receiving the average runtime over 3 runs

### As a module
#### run_filter
Import: `import instapy.cli` \
Called with: `instapy.cli.run_filter`

Contains:
`run_filter`

`run_filter` requires a filename for an image, and an output file if you want to save the image. Choose the implementation and filter you want to use with respectively `implementation=` `"python"`, `"numpy"` or `"numba"` and `filter=` `"color2gray"` or `"color2sepia"`

#### \<implementation\>_filters
Import: `import instapy.<implementation>_filters` \
Called with: `instapy.<implementation>_filters.<implementation>_<filter>`

Contains: \
`python_filters` \
`numpy_filters` \
`numba_filters`

which each contain the filters: \
`color2gray` \
`color2sepia`

Each function takes the array version of an image, which can be obtained with `instapy.io.read_image(filename)`, and returns the array version of the filtered image. This can be displayed using `instapy.io.display(image)` or saved using `instapy.io.write_image(image)`.

Example:
```python
from instapy import io
import instapy.numpy_filters

image = io.read_image("rain.jpg")
filtered_image = instapy.numpy_filters.numpy_sepia(image)
io.display(filtered_image)
```
This is the same as running
```python
from instapy import cli

cli.run_filter("rain.jpg", implementation="numpy", filter="sepia")
```

## Extra notes:
Using `pytest` generally works, other than when comparing the filtered images generated from the different implementations. This is due to a couple of pixels in the entire image having a difference of 1, although it sometimes runs without errors.

Note `timing-report.txt` differentiates between the first call, and the average after. This is due to numba using a lot of time to compile the first time, and therefore doesn't reflect the time gained. It is worth noting that the time from the first call might be the one which most accurately reflects real world use, as you would usually only apply the filters one at a time.
