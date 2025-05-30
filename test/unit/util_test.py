import unittest
import pytest

from app import util
from app.util import InvalidConvertToNumber 


@pytest.mark.unit
class TestUtil(unittest.TestCase):
    def test_convert_to_number_correct_param(self):
        self.assertEqual(4, util.convert_to_number("4"))
        self.assertEqual(0, util.convert_to_number("0"))
        self.assertEqual(0, util.convert_to_number("-0"))
        self.assertEqual(-1, util.convert_to_number("-1"))
        self.assertAlmostEqual(4.0, util.convert_to_number("4.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("0.0"), delta=0.0000001)
        self.assertAlmostEqual(0.0, util.convert_to_number("-0.0"), delta=0.0000001)
        self.assertAlmostEqual(-1.0, util.convert_to_number("-1.0"), delta=0.0000001)

    def test_convert_to_number_invalid_type(self):
        self.assertRaises(TypeError, util.convert_to_number, "")
        self.assertRaises(TypeError, util.convert_to_number, "3.h")
        self.assertRaises(TypeError, util.convert_to_number, "s")
        self.assertRaises(TypeError, util.convert_to_number, None)
        self.assertRaises(TypeError, util.convert_to_number, object())
        
    def test_invalid_convert_to_number_with_int(self):
        assert InvalidConvertToNumber("42") == 42

    def test_invalid_convert_to_number_with_float(self):
        assert InvalidConvertToNumber("3.14") == 3.14

    def test_invalid_convert_to_number_with_invalid(self):
        with self.assertRaises(TypeError):
            InvalidConvertToNumber("not_a_number")
            
    def test_validate_permissions_user1(self):
        result = util.validate_permissions("sum", "user1")
        self.assertTrue(result)

    def test_validate_permissions_other_user(self):
        result = util.validate_permissions("sum", "otro_usuario")
        self.assertFalse(result)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()