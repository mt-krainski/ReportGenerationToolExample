This is a simple command line tool to generate html reports from a predefined
Jupyter Notebooks. The standard flow would be that you create a report template
and then you can, using just the command line interface, easily replace
the description and parsed file in the generated report.

Usage example:
``python ./generate_report.py --filename test_data/testFileA.csv --kernel-name python3 -o result.html --description "This is my test description"``

TODO:

* improve readme
* add requirements.txt
* add more detailed comments
