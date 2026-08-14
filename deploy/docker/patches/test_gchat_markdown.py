"""Unit tests for the Google Chat Markdown rendering installed by the Dockerfile.

Run: python3 -m unittest discover -s deploy/docker/patches -p 'test_*.py' -t deploy/docker/patches

``AGENT_REPLY`` is the message that was fed to the deployed adapter on
2026-08-14 to establish what was actually broken, and the two defects it
exposed — a flattened nested list and a raw pipe table — are what this module
pins. It is kept verbatim rather than trimmed to the assertion, because the
point is that an ordinary fleet-status reply triggers both.
"""

import unittest

from gchat_markdown import (
    MAX_TABLE_WIDTH,
    collapse_interior_spaces,
    convert_rules,
    convert_tables,
)

AGENT_REPLY = """\
Here are the clusters:

| Cluster | Nodes | Status |
| --- | --- | --- |
| prod-east | 12 | Healthy |
| staging | 3 | Degraded |

Next steps:

- Check the autoscaler
  - Review the node pool
- Escalate if unresolved
"""


def _identity(value):
    """Stand-in for ``format_message``'s ``_ph``: protect without placeholders."""
    return value


class ConvertTablesTest(unittest.TestCase):
    def test_columns_are_padded_to_equal_width(self):
        out = convert_tables(AGENT_REPLY, _identity)
        rows = [ln for ln in out.splitlines() if ln.startswith("| ")]
        self.assertEqual(len({len(row) for row in rows}), 1, out)

    def test_table_is_fenced_so_chat_renders_it_monospaced(self):
        out = convert_tables(AGENT_REPLY, _identity)
        self.assertIn("```\n| Cluster   | Nodes | Status   |", out)
        self.assertTrue(out.count("```") >= 2)

    def test_prose_around_the_table_is_untouched(self):
        out = convert_tables(AGENT_REPLY, _identity)
        self.assertIn("Here are the clusters:", out)
        self.assertIn("- Escalate if unresolved", out)

    def test_result_is_protected_from_later_rewrites(self):
        seen = []

        def protect(value):
            seen.append(value)
            return "\x00PH\x00"

        out = convert_tables(AGENT_REPLY, protect)
        self.assertEqual(len(seen), 1)
        self.assertIn("\x00PH\x00", out)
        # The padding only survives format_message if it went through _ph.
        self.assertIn("| prod-east | 12    | Healthy  |", seen[0])

    def test_alignment_markers_are_honoured(self):
        # Cells must be wider than one character for alignment to be visible.
        table = "| Count | State |\n| ---: | :---: |\n| 7 | ok |\n"
        out = convert_tables(table, _identity)
        self.assertIn("| Count | State |", out)
        self.assertIn("|     7 |   ok  |", out)

    def test_short_row_does_not_raise(self):
        table = "| a | b | c |\n| --- | --- | --- |\n| 1 |\n"
        out = convert_tables(table, _identity)
        self.assertIn("| 1 |", out)

    def test_wide_table_falls_back_to_stanzas(self):
        wide = "x" * 80
        table = f"| Cluster | Detail |\n| --- | --- |\n| prod-east | {wide} |\n"
        out = convert_tables(table, _identity)
        self.assertNotIn("```", out)
        self.assertIn("*prod-east*", out)
        self.assertIn(f"  Detail: {wide}", out)

    def test_grid_is_used_right_up_to_the_width_limit(self):
        table = "| a | b |\n| --- | --- |\n| 1 | 2 |\n"
        out = convert_tables(table, _identity)
        self.assertIn("```", out)
        widest = max(len(ln) for ln in out.splitlines())
        self.assertLessEqual(widest, MAX_TABLE_WIDTH)

    def test_text_without_pipes_is_returned_unchanged(self):
        text = "no tables here\njust prose\n"
        self.assertEqual(convert_tables(text, _identity), text)

    def test_horizontal_rule_is_not_read_as_a_table(self):
        text = "before\n\n---\n\nafter\n"
        self.assertEqual(convert_tables(text, _identity), text)


class ConvertRulesTest(unittest.TestCase):
    def test_rule_becomes_a_divider(self):
        self.assertIn("─", convert_rules("a\n---\nb"))

    def test_setext_underline_is_not_a_rule_when_it_has_text(self):
        self.assertEqual(convert_rules("a - b"), "a - b")

    def test_asterisk_and_underscore_rules_convert(self):
        self.assertIn("─", convert_rules("***"))
        self.assertIn("─", convert_rules("___"))


class CollapseInteriorSpacesTest(unittest.TestCase):
    def test_leading_indentation_survives(self):
        text = "- top\n  - nested\n    - deeper"
        self.assertEqual(collapse_interior_spaces(text), text)

    def test_interior_double_space_is_still_collapsed(self):
        self.assertEqual(collapse_interior_spaces("a  b"), "a b")

    def test_the_upstream_regression_is_pinned(self):
        # The exact defect measured on the deployed adapter: two-space indent
        # arriving as one. re.sub(r"  +", " ", ...) produced " - Review".
        text = "- Check the autoscaler\n  - Review the node pool"
        self.assertIn("\n  - Review", collapse_interior_spaces(text))


if __name__ == "__main__":
    unittest.main()
