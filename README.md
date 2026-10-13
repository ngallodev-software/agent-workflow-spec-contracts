# Agent-Workflow Shared Contracts

## Summary

- **What it is:** the frozen, versioned compatibility contract package for the historical SpecGen → Agent-Workflow `native-job/v1` handoff.
- **Why it remains:** existing v1 jobs and sealed historical evidence must retain their original contract meaning while new Agent-Workflow planning moves to OpenSpec-backed `native-job/v2`.
- **Key boundary:** this package preserves legacy handoff semantics only; OpenSpec-backed v2 jobs do not negotiate or require it.
- **Versioning rule:** published semantic contract bytes are immutable; packaging-only changes can advance the distribution without redefining contract meaning.

`agent-workflow-spec-contracts` publishes the immutable, versioned semantic
contracts shared by [SpecGen](https://github.com/ngallodev-software/specgen-aw)
and [Agent-Workflow](https://github.com/ngallodev-software/agent-workflow).

Its purpose is deliberately narrow: preserve the meaning of the historical
SpecGen → Agent-Workflow v1 handoff in one dependency-neutral package so neither
repository has to rewrite previously published schemas or sealed evidence.

For new planning work, Agent-Workflow now has a qualified OpenSpec 1.13.2 import
path that produces Agent-Workflow-owned `native-job/v2` contracts. That path
does not negotiate this bundle. Retirement of this package as a mandatory
Agent-Workflow dependency is a separate compatibility change; the published
v1 bundle remains immutable.

## Ownership boundary

```text
human / repository intent
        |
        v
      SpecGen
        |
        |  versioned shared contracts
        v
agent-workflow-spec-contracts
        |
        v
   Agent-Workflow
        |
        v
execution / evidence / review / acceptance
```

- **SpecGen** owns specification authoring, evidence, requirements, acceptance
  intent, evaluation intent, and target compilation.
- **This package** owns the immutable shared schema/fixture bundle used at the
  handoff boundary.
- **Agent-Workflow** owns execution semantics, lifecycle authority, evidence,
  review, recovery, and acceptance.

A contract release therefore does not move workflow authority into this package;
it only versions the data meaning both sides agree to consume.

## Versioning

The published distribution is `v0.2.1`. It is a distribution-only patch
release carrying semantic bundle `0.2.0`; the schemas and contract meaning are
unchanged from that bundle.

Distribution versions and semantic bundle versions are intentionally distinct:

- a **semantic bundle** changes only when contract meaning changes;
- a **distribution patch** may repackage the same immutable semantic bundle;
- previously published semantic contract bytes are not rewritten in place.

The `v0.2.1` wheel is published as a GitHub Release asset rather than as a new
semantic bundle version.

## Install the immutable release

```bash
python -m pip install 'https://github.com/ngallodev-software/agent-workflow-spec-contracts/releases/download/v0.2.1/specgen_agent_workflow_contracts-0.2.1-py3-none-any.whl#sha256=d254a0b13f2fd1de732dab2abd33da35db9ea365b50b3214e92308fea79d85c2'
```

The pinned digest makes the exact contract distribution explicit for consumers
that need reproducible builds.

## Repository layout

- `src/specgen_contracts/schemas/` — versioned JSON schemas.
- `src/specgen_contracts/fixtures/` — shared contract fixtures.
- `docs/` — contract and integration documentation.
- `tests/` — validation for published package behavior.

## Build and test

```bash
python -m pip install -e .
python -m pytest
python -m build --wheel
```

The `contract-bundle` CLI is exposed by the package for inspecting the bundled
contracts.

## Related repositories

- [SpecGen](https://github.com/ngallodev-software/specgen-aw)
- [Agent-Workflow](https://github.com/ngallodev-software/agent-workflow)
- [Agent-Workflow Benchmark](https://github.com/ngallodev-software/agent-workflow-benchmark)
