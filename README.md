SEAS5 Causality
==============================
[![Build Status](https://github.com/nenb/seas5_causality/workflows/Tests/badge.svg)](https://github.com/nenb/seas5_causality/actions)
[![codecov](https://codecov.io/gh/nenb/seas5_causality/branch/master/graph/badge.svg)](https://codecov.io/gh/nenb/seas5_causality)
[![License:MIT](https://img.shields.io/badge/License-MIT-lightgray.svg?style=flt-square)](https://opensource.org/licenses/MIT)[![pypi](https://img.shields.io/pypi/v/seas5_causality.svg)](https://pypi.org/project/seas5_causality)
[![Documentation Status](https://readthedocs.org/projects/seas5_causality/badge/?version=latest)](https://seas5_causality.readthedocs.io/en/latest/?badge=latest)


### A project exploring the use of causality tools in the ECMWF SEAS5 forecast model.

--------

The main results so far are contained in the `notebooks` subdirectory.

To view the results on your local machine, first clone this repository:

``` bash
git clone https://github.com/nenb/seas5_causality
```

The project dependcies are managed via [CONDA](https://docs.conda.io/en/latest/). From the project root directory:

```bash
conda env create -f environment.yml
conda activate seas5_causality
```

That's it for the setup. You can now go ahead and view my analysis:

```bash
cd notebooks
jupyter-lab
```

<hr>

To reproduce the images is a bit more involved. You will need to download both ERA5 and SEAS5 data.
The scripts to do this are located in the `scripts` subdirectory. To use these scripts, you will need to have both a
[Copernicus](https://cds.climate.copernicus.eu/#!/home) account and a [MARS](https://www.ecmwf.int/en/forecasts/accessing-forecasts) account.

The source code to produce the images from the data is located in the `seas5_causality` subdirectory.

<hr>

<p><small>Project based on the <a target="_blank" href="https://github.com/jbusecke/cookiecutter-science-project">cookiecutter science project template</a>.</small></p>
