# Supported versions

Bundle `0.2.0` is the supported semantic release. Its published Python
distribution is `0.2.1`, a distribution-only patch carrying semantic bundle
`0.2.0` and published as a GitHub Release wheel asset. It does not introduce
bundle `0.2.1` or change any shared schema bytes or meaning.

Releases are immutable: a
change to shared meaning, schema bytes, IDs, or canonicalization requires a
new semantic-versioned release and an explicit deterministic migration from
each supported prior release. Unknown versions and schema digests fail closed.
The sole supported migration is an `agent-workflow/prompt-pack/v1` document
from bundle `0.1.0` to the v2 prompt-pack in bundle `0.2.0`.

The bundle owns only the documented shared contract surface. It does not own
authoring, compilation, scheduling, workers, lifecycle, evaluation, review,
acceptance, sealing, persistence, or generic CRUD.
