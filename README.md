# Agent-Workflow shared contracts

Immutable, versioned semantic contracts consumed by SpecGen and Agent-Workflow.

## Build and test

```bash
python -m pip install -e .
python -m pytest
python -m build --wheel
```

Tagged releases (`vX.Y.Z`) publish the matching wheel to the GitHub Packages
Python registry. Consumers must provide a token with `read:packages`:

```bash
export PIP_EXTRA_INDEX_URL="https://USERNAME:TOKEN@pypi.pkg.github.com/ngallodev-software/simple/"
python -m pip install 'specgen-agent-workflow-contracts==0.2.0'
```
