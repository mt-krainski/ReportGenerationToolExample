This is a simple command line tool to generate html reports from a predefined
Jupyter Notebooks. The standard flow would be that you create a report template
and then you can, using just the command line interface, easily replace
the description and parsed file in the generated report.

Install all dependencies with:

``pip install -r requirements.txt``

This requires Python 3.6+

Usage example:

``python ./generate_report.py --filename test_data/testFileA.csv --kernel-name python3 --output result.html --description "This is my test description"``

After that, a new result.html file will be created.

When using virtual environments be sure to create an ipython kernel for that environment with:

``python -m ipykernel install --user --name my_env --display-name "Python (my_env)"``

And change the value ``--kernel-name`` parameter to ``my_env``.

TODO:

* improve readme
* add more detailed comments
