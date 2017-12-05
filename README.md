
This notebook was used to demo some plotting libraries at BioInfoSummer 2017 and in my [PyConAU 2017 talk](https://www.youtube.com/watch?v=6d3Yk7a2qYI).

If you'd like to run this Jupyter Notebook and/or Dash app yourself, you should be able to install all required packages using:

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Depending on what version of Jupyter you're running, you may need to launch this notebook with a higher data rate limit so that visualisation libraries are not throttled in communicating with the browser, e.g.

```jupyter notebook --NotebookApp.iopub_data_rate_limit=10000000```

This issue is referenced [here](https://github.com/jupyter/notebook/issues/2287).
