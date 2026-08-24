import textwrap
import unittest

from bump_version import get_next_version, set_version


def fixture(s: str) -> str:
    return textwrap.dedent(s).strip()


class TestGetNextVersion(unittest.TestCase):
    def test_next_version(self):
        cases = (
            ("v0.0.0", "patch", "0.0.1"),
            ("v0.0.0", "minor", "0.1.0"),
            ("v1.2.3", "patch", "1.2.4"),
            ("v1.2.3", "minor", "1.3.0"),
            ("v1.2.3", "major", "2.0.0"),
        )

        for tag, strategy, expected in cases:
            with self.subTest(tag=tag, strategy=strategy):
                self.assertEqual(get_next_version(tag, strategy), expected)


class TestSetVersion(unittest.TestCase):
    def test_update_version(self):
        src = fixture("""
            ---
            name: temporal-developer
            description: The Temporal Developer skill
            version: 0.5.0
            ---
            """)
        expected = fixture("""
            ---
            name: temporal-developer
            description: The Temporal Developer skill
            version: 0.5.1
            ---
            """)
        self.assertEqual(set_version(src, "0.5.1"), expected)

    def test_add_version(self):
        src = fixture("""
            ---
            name: temporal-developer
            description: The Temporal Developer skill
            ---
            """)
        expected = fixture("""
            ---
            name: temporal-developer
            description: The Temporal Developer skill
            version: 0.1.0
            ---
            """)
        self.assertEqual(set_version(src, "0.1.0"), expected)

    def test_rejects_missing_frontmatter(self):
        with self.assertRaises(ValueError):
            set_version("# Skill\n", "1.0.0")


if __name__ == "__main__":
    unittest.main()
