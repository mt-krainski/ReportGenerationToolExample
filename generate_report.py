import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename",
    help="ERICA's log file to be parsed. If empty, will use the most recent.",
    required=True)
parser.add_argument("-d", "--description",
    default="--",
    help="This is the description of this test, "
         "it will be included in the report")
parser.add_argument("-k", "--kernel-name",
    default="Python3",
    help="Defines the ipython kernel to be used for executing the notebook")
parser.add_argument("-o", "--output",
    default="_report",
    help="Defines the name of created html report file")

script_arguments = parser.parse_args()

import nbparameterise
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import subprocess
import sys
APPNAME = 'generate_report'

if ".html" in script_arguments.output:
    script_arguments.output = script_arguments.output[0:-5]

RESULT_FILENAME = script_arguments.output + '.ipynb'

print('[{}] Reading template...'.format(APPNAME))
with open("report_template.ipynb") as f:
    nb = nbformat.read(f, as_version=4)

orig_parameters = nbparameterise.extract_parameters(nb)

ep = ExecutePreprocessor(
    timeout=600,
    kernel_name=script_arguments.kernel_name)

params = nbparameterise.parameter_values(
    orig_parameters,
    test_filename=script_arguments.filename,
    description=script_arguments.description)

print('[{}] Replacing parameters...'.format(APPNAME))
new_nb = nbparameterise.replace_definitions(nb, params, execute=False)

print('[{}] Executing notebook...'.format(APPNAME))
_ = ep.preprocess(new_nb, {'metadata': {'path': '.'}})

print('[{}] Saving notebook to temporary file...'.format(APPNAME))
with open(RESULT_FILENAME, 'wt') as f:
    nbformat.write(new_nb, f)

try:
    print('[{}] Converting to html...'.format(APPNAME))
    subprocess.call(['jupyter', 'nbconvert', RESULT_FILENAME, '--to', 'html'])

finally:
    print('[{}] Deleting {}...'.format(APPNAME, RESULT_FILENAME))
    if sys.platform == 'win32':
        subprocess.call(['del', RESULT_FILENAME], shell=True)
    else:
        subprocess.call(['rm {}'.format(RESULT_FILENAME)], shell=True)
