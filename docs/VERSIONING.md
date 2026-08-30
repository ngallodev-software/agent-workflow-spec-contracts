# Supported versions

Bundle `0.1.0` is the only supported release. Releases are immutable: a
change to shared meaning, schema bytes, IDs, or canonicalization requires a
new semantic-versioned release and an explicit deterministic migration from
each supported prior release. Unknown versions and schema digests fail closed.

The bundle owns only the documented shared contract surface. It does not own
authoring, compilation, scheduling, workers, lifecycle, evaluation, review,
acceptance, sealing, persistence, or generic CRUD.
