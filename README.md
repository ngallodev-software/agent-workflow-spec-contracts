# Agent-Workflow Spec Contracts

Immutable, versioned semantic contracts shared by SpecGen and Agent-Workflow
(release 0.2.0).

The public package is `specgen_contracts`. It provides schema lookup and
digests, deterministic JSON normalization, validation diagnostics, artifact
descriptors, version negotiation, and explicit migrations. Install the wheel
and use `contract-bundle validate SCHEMA_ID DOCUMENT.json` or
`contract-bundle digest SCHEMA_ID`.
