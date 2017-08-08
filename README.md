# Data-Chan Python

[![wercker status](https://app.wercker.com/status/1fb1f6cc68959c13ef6b477ce7abefff/s/master "wercker status")](https://app.wercker.com/project/byKey/1fb1f6cc68959c13ef6b477ce7abefff)

Data-Chan-python allows you to use the [data-chan](https://github.com/neroreflex/data-chan) comunication library with Python and [Jupyter](http://jupyter.org/).

### Releasing

To release, just bump the version and push to master. Wercker-CI will take care of the build and deploy process.

``` shell
pip install bump

# Bump patch/major/minor
bump setup.py -b
bump setup.py -m
bump setup.py -M

# Create .tar.gz archive
python setup.py sdist

# Upload to PyPi the latest file
twine upload dist/$(ls -tp dist | grep -v /$ | head -1)
```
