# Agent-Workflow shared contracts

Immutable, versioned semantic contracts consumed by SpecGen and Agent-Workflow.

## Build and test

```bash
python -m pip install -e .
python -m pytest
python -m build --wheel
```

The published distribution is `v0.2.1`. This is a distribution-only patch
release: it carries semantic bundle `0.2.0`, whose schemas and contract
meaning are unchanged. The `v0.2.1` wheel is published as a GitHub Release
asset, not as a new semantic bundle version.

Download the wheel from the GitHub Release and install it directly:

```bash
python -m pip install ./specgen_agent_workflow_contracts-0.2.1-py3-none-any.whl
```
