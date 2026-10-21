# mini-deep-merge

Merge nested mappings with explicit rules for lists and nulls.

```python
from mini_deep_merge import deep_merge

base = {"db": {"host": "localhost", "port": 5432}, "tags": ["a"]}
patch = {"db": {"port": 5433}, "tags": ["b", "c"]}

result = deep_merge(base, patch)
# {'db': {'host': 'localhost', 'port': 5433}, 'tags': ['b', 'c']}
```

## Why

Configuration is often layered: defaults, environment overrides, user
preferences. When the values are flat scalars, merging is obvious. When the
values are nested dicts, a shallow merge discards the lower layer entirely,
which is rarely what anyone wants. This library exists to do the recursive
dict merge correctly and to stop there.

The trade-off is that lists and nulls are not smart. Lists are replaced, never
concatenated — concatenation needs domain knowledge (deduplicate? preserve
order? match by id?) that a generic library cannot guess. ``None`` in the
patch overwrites the base value; it is not a sentinel meaning "delete this key".

## Edge cases you will hit

- A dict in the patch replacing a scalar (or a list) in the base: the dict
  wins wholesale.
- A scalar (or a list) in the patch replacing a dict in the base: same, the
  patch value wins.
- ``None`` in the patch: it is a literal value, so it overwrites. If you need
  deletions, strip the keys yourself before merging.

## API

- `deep_merge(a: Mapping, b: Mapping) -> dict` — recursively merge `b` into
  `a`. Neither input is mutated. Returns a new dict.
