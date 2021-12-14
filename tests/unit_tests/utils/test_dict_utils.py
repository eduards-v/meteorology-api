from unittest import TestCase

from utils.dict_utils import nest_flat_dict

ORIGINAL = {'sens_id': 1, 'city_name': 'Galway', 'country_name': 'Ireland'}


class TestDictUtils(TestCase):
    def test_nest_flat_dict_return(self):
        mutated = nest_flat_dict(ORIGINAL, "metadata", "country_name", "city_name")

        self.assertIsInstance(mutated, dict)
        self.assertNotEqual(mutated, ORIGINAL)
        self.assertTrue(mutated.get("metadata"))
        self.assertIsInstance(mutated["metadata"], dict)
        self.assertEqual(mutated["metadata"], {'city_name': 'Galway', 'country_name': 'Ireland'})

    def test_nest_flat_dict_input_not_dict(self):
        original = [1, 'Galway', 'Ireland']
        with self.assertRaises(AssertionError):
            nest_flat_dict(original, "metadata")

    def test_nest_flat_dict_input_invalid_key_arg(self):
        with self.assertRaises(AssertionError):
            nest_flat_dict(ORIGINAL, "metadata", "wrong_key", "country_name", "city_name")

    def test_nest_flat_dict_original_preserved(self):
        mutated = nest_flat_dict(ORIGINAL, "metadata", "country_name", "city_name")
        self.assertEqual(ORIGINAL, ORIGINAL)

    def test_nest_flat_dict_with_empty_subdict(self):
        mutated = nest_flat_dict(ORIGINAL, "metadata")
        self.assertFalse(mutated["metadata"])
