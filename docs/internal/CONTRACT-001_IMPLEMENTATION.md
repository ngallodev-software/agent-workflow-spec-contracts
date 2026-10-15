# CONTRACT-001 implementation contract

## Scope

Release bundle `0.2.0`. Preserve `agent-workflow/prompt-pack/v1` schema bytes
unchanged and add `agent-workflow/prompt-pack/v2` with required structured
`bundle_provenance`:

```json
{"bundle_version":"0.2.0","schema_id":"agent-workflow/prompt-pack/v2","schema_digest":"<sha256>"}
```

The bundle validates, describes, and negotiates both versions. Its only
supported migration is v1 pack to v2 pack. It must copy the caller document,
add a descriptor derived from the v2 schema, validate the result, and return
source/target descriptors. Unsupported migrations fail with an actionable
manual-migration error. No input bytes may be mutated.

## Application seams

SpecGen `0.2.0` pins bundle `==0.2.0` and emits a v2 pack with structured
provenance. Agent-Workflow `0.9.1` pins bundle `==0.2.0`; it accepts legacy
v1 packs through its existing local validator, validates v2 packs with the
bundle, and negotiates v2 provenance before creating mutable Agent Run state.

## Required proof

- exact installed producer/consumer v2 acceptance;
- substituted bundle version and digest rejection before preparation;
- v1-to-v2 migration with source and target descriptors;
- unsupported migration fails closed with `manual migration` wording;
- input sealed-source bytes are unchanged;
- v1 validation remains supported.

The bundle remains free of lifecycle, scheduling, repository, or authoring
code. Do not publish externally.
