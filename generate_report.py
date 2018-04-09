import nbparameterise
import nbformat

with open("Untitled.ipynb") as f:
    nb = nbformat.read(f, as_version=4)


params = nbparameterise.extract_parameters(nb)

print(params)
