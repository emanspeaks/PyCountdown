# PyCountdown

MCC-style countdown clocks

## Documentation

See the [User Manual](docs/user_guide.md) for comprehensive usage instructions.

## Develop

### Automatic versioning

If you need to test features that require a version number prior to creating a tag, you can override the automatic versioning by creating a Python module `pycountdown._version` that exports `__version__`.  When this file is absent or does not contain a `__version__` attribute, it reverts to dynamic versioning. Note that `hatchling build` automatically generates the `pycountdown._version` module when the package is built, so versions deployed to PyPI should have the hardcoded versions via these files.  Similarly, though, if you are starting from a version of the package that has one of these hardcoded files, simply delete it to again go back to dynamic versioning.

Note that the dynamic versioning really only works when `hatchling` and `hatch-vcs` are installed.
If either of these packages are not installed, it attempts to read the version from the installed package metadata.
However, any value in `pycountdown._version.__version__` will always override both of these.

<!-- When a pull request is opened against the main branch, this will trigger a push to test.pypi.org.  However, the GitHub Actions workflow is configured to publish only on `pull_request`, which checks out the git repo AFTER a temporary merge to main, so it has an extra merge commit in the history and increments the dev version by one when doing the Hatch build.  This means that the dev version on test.pypi.org may be a different dev number than what appears in a local repo when running `hatch version` or otherwise getting the dynamic version from the package in Python. -->
