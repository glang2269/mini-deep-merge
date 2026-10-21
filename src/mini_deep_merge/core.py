"""Deep merge for nested mappings.

Design decisions (stated plainly so the behaviour is unambiguous):

- Only dicts are merged recursively. A dict in ``b`` merged into a non-dict in
  ``a`` is replaced wholesale by the dict from ``b``; we do not try to coerce.
- Lists are replaced, not concatenated. Concatenation requires domain
  knowledge (deduplication? ordering? identity?) that a generic merge cannot
  guess at, so the chosen rule is: last list wins.
- ``None`` in ``b`` is treated as a value, not as a deletion sentinel. There is
  no schema from which to know whether ``None`` means "unset" or "explicitly
  empty", so it is treated literally and overwrites.
"""

from typing import Any, Mapping


def deep_merge(a: Mapping[str, Any], b: Mapping[str, Any]) -> dict:
    """Recursively merge mapping ``b`` into mapping ``a``.

    Neither input is mutated; the returned dict is always new. For keys present
    in both, when *both* values are dicts they are merged recursively;
    otherwise the value from ``b`` wins.
    """
    result: dict = {**a}
    for key, b_value in b.items():
        a_value = result.get(key)
        if isinstance(a_value, dict) and isinstance(b_value, dict):
            # Recursive case is the entire point of the library.
            result[key] = deep_merge(a_value, b_value)
        else:
            # Last-write-wins is the only rule that does not require guessing
            # the caller's intent for lists, scalars, and None.
            result[key] = b_value
    return result
