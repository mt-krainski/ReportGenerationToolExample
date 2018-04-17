import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename",
    help="ERICA's log file to be parsed. If empty, will use the most recent.",
    required=True)
parser.add_argument("-d", "--description",
    default="--",
    help="This is the description of this test, "
         "it will be included in the report")

script_arguments = parser.parse_args()

import nbparameterise
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import subprocess
import sys
APPNAME = 'create_report'

with open("report_template.ipynb") as f:
    nb = nbformat.read(f, as_version=4)


orig_parameters = nbparameterise.extract_parameters(nb)

ep = ExecutePreprocessor(
    timeout=600,
    kernel_name=nb.metadata.get('kernelspec', {}).get('name', 'python3'))

params = nbparameterise.parameter_values(
    orig_parameters,
    testfile_name=script_arguments.filename,
    description=script_arguments.description)

new_nb = nbparameterise.replace_definitions(nb, params, execute=False)

_ = ep.preprocess(new_nb, {'metadata': {'path': '.'}})
RESULT_FILENAME = "_report.ipynb"
with open(RESULT_FILENAME, 'wt') as f:
    nbformat.write(new_nb, f)

try:
    # Convert to html
    print('[{}] Converting to html'.format(APPNAME))
    subprocess.call(['jupyter', 'nbconvert', RESULT_FILENAME, '--to', 'html'])

finally:
    # Delete unnecessary notebook file
    print('[{}] Deleting {}'.format(APPNAME, RESULT_FILENAME))
    if sys.platform == 'win32':
        subprocess.call(['del', RESULT_FILENAME], shell=True)
    else:
        subprocess.call(['rm {}'.format(RESULT_FILENAME)], shell=True)
