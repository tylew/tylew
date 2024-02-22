import unittest
from unittest.mock import patch
from day1_lab import * 

class TestDay1Problems(unittest.TestCase):

    def test_problem_01(self):
        with patch('builtins.print') as mocked_print:
            problem_1()
            mocked_print.assert_called_with(4)

    def test_problem_02(self):
        self.assertEqual(problem_2(5), 10)
        self.assertEqual(problem_2(-5), 0)
        self.assertEqual(problem_2(0), 5)
        self.assertEqual(problem_2(100), 105)

    def test_problem_03(self):
        with patch('builtins.print') as mocked_print:
            problem_3("Hello", "World")
            mocked_print.assert_has_calls([unittest.mock.call("Hello"), unittest.mock.call("World")])
            problem_3("Foo", "Bar")
            mocked_print.assert_has_calls([unittest.mock.call("Foo"), unittest.mock.call("Bar")])
            problem_3("Python", "Rocks")
            mocked_print.assert_has_calls([unittest.mock.call("Python"), unittest.mock.call("Rocks")])
            problem_3("Test", "Case")
            mocked_print.assert_has_calls([unittest.mock.call("Test"), unittest.mock.call("Case")])

    def test_problem_04(self):
        self.assertTrue(problem_4(2))
        self.assertFalse(problem_4(3))
        self.assertTrue(problem_4(0))
        self.assertFalse(problem_4(-1))
        self.assertTrue(problem_4(100))
        self.assertFalse(problem_4(101))
        self.assertTrue(problem_4(-2))
        self.assertFalse(problem_4(-3))

    def test_problem_05(self):
        self.assertTrue(problem_5(3))
        self.assertFalse(problem_5(4))
        self.assertTrue(problem_5(0))
        self.assertFalse(problem_5(-2))
        self.assertTrue(problem_5(9))
        self.assertFalse(problem_5(10))
        self.assertTrue(problem_5(-3))
        self.assertFalse(problem_5(-4))

    def test_problem_06(self):
        self.assertTrue(problem_6(3))
        self.assertTrue(problem_6(5))
        self.assertFalse(problem_6(7))
        self.assertTrue(problem_6(0))
        self.assertTrue(problem_6(15))
        self.assertFalse(problem_6(16))
        self.assertTrue(problem_6(-3))
        self.assertTrue(problem_6(-5))

    def test_problem_07(self):
        self.assertEqual(problem_7(3, 5), 5)
        self.assertEqual(problem_7(-3, -5), -3)
        self.assertEqual(problem_7(3, 3), 3)
        self.assertEqual(problem_7(0, 0), 0)

    def test_problem_08(self):
        self.assertEqual(problem_8(3, 5, 1), 1)
        self.assertEqual(problem_8(3, 3, 3), 3)
        self.assertEqual(problem_8(1, 2, 3), 1)
        self.assertEqual(problem_8(0, 0, 0), 0)

    def test_problem_09(self):
        self.assertEqual(problem_9([1, 2, 3]), 3)
        self.assertEqual(problem_9(["a", "b", "c"]), "c")
        self.assertEqual(problem_9([1, 2, 3, 4]), 3)
        self.assertEqual(problem_9(["apple", "banana", "cherry"]), "cherry")

    def test_problem_10(self):
        self.assertEqual(problem_10([1, 2, 3]), 1)
        self.assertEqual(problem_10(["a", "b", "c"]), "a")
        self.assertEqual(problem_10([3, 2, 1]), 1)
        self.assertEqual(problem_10(["c", "b", "a"]), "a")

    def test_problem_11(self):
        self.assertEqual(problem_11([1, 2, 3]), 3)
        self.assertEqual(problem_11([]), 0)
        self.assertEqual(problem_11([1]), 1)
        self.assertEqual(problem_11([1, 2, 3, 4]), 4)

    def test_problem_12(self):
        self.assertEqual(problem_12([1, 2, 3], 2), 1)
        self.assertIsNone(problem_12([1, 2, 3], 4))
        self.assertEqual(problem_12(["a", "b", "c"], "b"), 1)
        self.assertIsNone(problem_12(["a", "b", "c"], "d"))

    def test_problem_13(self):
        self.assertEqual(problem_13([1, 2, 3, 4, 5]), 8)
        self.assertEqual(problem_13([1, 2]), 0)
        self.assertEqual(problem_13(["a", "b", "c", "d", "e"]), "ce")
        self.assertEqual(problem_13([1, 2, 3]), 0)
        self.assertEqual(problem_13([0, 0, 0, 0, 0]), 0)
        self.assertEqual(problem_13([1, 1, 1, 1, 1]), 2)
        self.assertEqual(problem_13([-1, -2, -3, -4, -5]), -8)
        self.assertEqual(problem_13([1, 2, 3, 4, 5, 6]), 8)

    def test_problem_14(self):
        self.assertEqual(problem_14([1, 2, 3, 4, 5]), 9)
        self.assertEqual(problem_14([]), 0)
        self.assertEqual(problem_14([1]), 1)
        self.assertEqual(problem_14([1, 2]), 1)
        self.assertEqual(problem_14([0, 0, 0]), 0)
        self.assertEqual(problem_14([-1, -2, -3]), -4)
        self.assertEqual(problem_14([1, 1, 1]), 2)
        self.assertEqual(problem_14([1, 2, 3, 4, 5, 6]), 9)

    def test_problem_15(self):
        self.assertEqual(problem_15([1, 2, 3, 4, 5, 6]), 9)
        self.assertEqual(problem_15([1, 2]), 0)
        self.assertEqual(problem_15([1, 2, 3]), 3)
        self.assertEqual(problem_15([1, 2, 3, 4]), 3)
        self.assertEqual(problem_15([0, 0, 0]), 0)
        self.assertEqual(problem_15([-1, -2, -3]), -3)
        self.assertEqual(problem_15([1, 1, 1]), 1)
        self.assertEqual(problem_15([1, 2, 3, 4, 5, 6, 7]), 9)

    def test_problem_16(self):
        self.assertEqual(problem_16(5), 15)
        self.assertEqual(problem_16(0), 0)
        self.assertEqual(problem_16(1), 1)
        self.assertEqual(problem_16(10), 55)
        self.assertEqual(problem_16(2), 3)
        self.assertEqual(problem_16(3), 6)
        self.assertEqual(problem_16(4), 10)
        self.assertEqual(problem_16(6), 21)

    def test_problem_17(self):
        self.assertEqual(problem_17(10), 33)
        self.assertEqual(problem_17(0), 0)
        self.assertEqual(problem_17(1), 0)
        self.assertEqual(problem_17(3), 3)
        self.assertEqual(problem_17(5), 8)
        self.assertEqual(problem_17(6), 14)
        self.assertEqual(problem_17(9), 23)
        self.assertEqual(problem_17(11), 33)

    def test_problem_18(self):
        self.assertEqual(problem_18("Hello World"), 3)
        self.assertEqual(problem_18("aeiou"), 5)
        self.assertEqual(problem_18("AEIOU"), 5)
        self.assertEqual(problem_18(""), 0)
        self.assertEqual(problem_18("HELLO"), 2)
        self.assertEqual(problem_18("WORLD"), 1)
        self.assertEqual(problem_18("Python"), 1)
        self.assertEqual(problem_18("Programming"), 3)

    def test_problem_19(self):
        self.assertEqual(problem_19("Hello World"), "Hll Wrld")
        self.assertEqual(problem_19("aeiou"), "")
        self.assertEqual(problem_19("AEIOU"), "")
        self.assertEqual(problem_19(""), "")
        self.assertEqual(problem_19("HELLO"), "HLL")
        self.assertEqual(problem_19("WORLD"), "WRLD")
        self.assertEqual(problem_19("Python"), "Pythn")
        self.assertEqual(problem_19("Programming"), "Prgrmmng")

    def test_problem_20(self):
        self.assertEqual(problem_20("Hello", "World"), "HWeolrllod")
        self.assertEqual(problem_20("abc", "123"), "a1b2c3")
        self.assertEqual(problem_20("abc", ""), "abc")
        self.assertEqual(problem_20("", "123"), "123")
        self.assertEqual(problem_20("a", "1"), "a1")
        self.assertEqual(problem_20("ab", "12"), "a1b2")
        self.assertEqual(problem_20("abc", "12"), "a1b2c")
        self.assertEqual(problem_20("ab", "123"), "a1b23")

    def test_problem_21(self):
        self.assertEqual(problem_21(1, 1, 1, 1), "square")
        self.assertEqual(problem_21(1, 2, 1, 2), "rectangle")
        self.assertEqual(problem_21(1, 2, 3, 4), "neither")
        self.assertEqual(problem_21(0, 1, 1, 1), "neither")
        self.assertEqual(problem_21(-1, 1, 1, 1), "neither")
        self.assertEqual(problem_21(1, 1, 1, 2), "neither")
        self.assertEqual(problem_21(2, 2, 2, 2), "square")
        self.assertEqual(problem_21(3, 4, 3, 4), "rectangle")
        self.assertEqual(problem_21(52, 52, 2, 2), "rectangle")
        self.assertEqual(problem_21(52, 4, 4, 52), "rectangle")
        self.assertEqual(problem_21(5, 52, 5, 52), "rectangle")
        self.assertEqual(problem_21(100, 100, 100, 100), "square")
        self.assertEqual(problem_21(-5, -5, -5, -5), "neither")


if __name__ == '__main__':
    unittest.main()