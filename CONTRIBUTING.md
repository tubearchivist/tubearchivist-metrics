## Contributing to Tube Archivist

Welcome, and thanks for showing interest in improving Tube Archivist!  
If you haven't already, the best place to start is the README. This will give you an overview on what the project is all about.

## Report a bug

If you notice something is not working as expected, check to see if it has been previously reported in the [open issues](https://github.com/tubearchivist/tubearchivist-metrics/issues).
If it has not yet been disclosed, go ahead and create an issue.  
If the issue doesn't move forward due to a lack of response, I assume it's solved and will close it after some time to keep the list fresh. 

## Dev setup

Setup your environment, e.g. with python venv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Setup pre-commit for linting:
```bash
pre-commit install
```
