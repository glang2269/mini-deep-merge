import unittest

from mini_deep_merge import deep_merge


class TestDeepMerge(unittest.TestCase):
    def test_disjoint_keys(self):
        self.assertEqual(deep_merge({"a": 1}, {"b": 2}), {"a": 1, "b": 2})

    def test_b_overwrites_scalar(self):
        self.assertEqual(deep_merge({"a": 1}, {"a": 2}), {"a": 2})

    def test_nested_dicts_merge(self):
        self.assertEqual(
            deep_merge({"a": {"x": 1}}, {"a": {"y": 2}}),
            {"a": {"x": 1, "y": 2}},
        )

    def test_b_dict_replaces_scalar(self):
        self.assertEqual(deep_merge({"a": 1}, {"a": {"x": 1}}), {"a": {"x": 1}})

    def test_scalar_replaces_b_dict(self):
        self.assertEqual(deep_merge({"a": {"x": 1}}, {"a": 2}), {"a": 2})

    def test_list_replaced_not_concatenated(self):
        self.assertEqual(deep_merge({"a": [1, 2]}, {"a": [3]}), {"a": [3]})

    def test_none_in_b_overwrites(self):
        self.assertEqual(deep_merge({"a": 1}, {"a": None}), {"a": None})

    def test_inputs_not_mutated(self):
        a = {"a": {"x": 1}}
        b = {"a": {"y": 2}}
        deep_merge(a, b)
        self.assertEqual(a, {"a": {"x": 1}})
        self.assertEqual(b, {"a": {"y": 2}})

    def test_deeply_nested(self):
        self.assertEqual(
            deep_merge({"a": {"b": {"c": 1}}}, {"a": {"b": {"d": 2}}}),
            {"a": {"b": {"c": 1, "d": 2}}},
        )

    def test_multiple_keys_mixed(self):
        self.assertEqual(
            deep_merge({"a": 1, "b": {"x": 1}}, {"b": {"y": 2}, "c": 3}),
            {"a": 1, "b": {"x": 1, "y": 2}, "c": 3},
        )

    def test_empty_b_returns_copy(self):
        a = {"a": 1}
        result = deep_merge(a, {})
        self.assertEqual(result, a)
        self.assertIsNot(result, a)

    def test_nested_list_is_replaced(self):
        self.assertEqual(
            deep_merge({"a": {"items": [1, 2]}}, {"a": {"items": [3]}}),
            {"a": {"items": [3]}},
        )

    def test_dict_in_b_replaces_dict_in_a_when_types_differ(self):
        self.assertEqual(
            deep_merge({"a": [1, 2]}, {"a": {"x": 1}}),
            {"a": {"x": 1}},
        )


if __name__ == "__main__":
    unittest.main()
