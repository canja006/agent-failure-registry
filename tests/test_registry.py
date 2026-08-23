import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import afr
from afr.model import invert


class TestModes(unittest.TestCase):
    def test_every_mode_loads(self):
        self.assertEqual(len(afr.modes()), 18)

    def test_lookup(self):
        m = afr.mode("AF-0142")
        self.assertEqual(m.title, "Stale context re-read")
        self.assertEqual(m.layer, "harness")

    def test_unknown_mode_raises(self):
        with self.assertRaises(KeyError):
            afr.mode("AF-9999")

    def test_layers_are_legal(self):
        for m in afr.modes():
            self.assertIn(m.layer, afr.LAYERS)

    def test_near_neighbors_resolve(self):
        ids = {m.id for m in afr.modes()}
        for m in afr.modes():
            for nn in m.near_neighbors:
                self.assertIn(nn, ids)


class TestRelations(unittest.TestCase):
    def test_inversion_is_involutive(self):
        for r in afr.RELATIONS:
            self.assertEqual(invert(invert(r)), r)

    def test_containment_flips(self):
        self.assertEqual(invert("broader"), "narrower")
        self.assertEqual(invert("narrower"), "broader")

    def test_symmetric_relations_hold(self):
        self.assertEqual(invert("exact"), "exact")
        self.assertEqual(invert("overlaps"), "overlaps")

    def test_bad_relation_rejected(self):
        with self.assertRaises(ValueError):
            invert("sortof")
        with self.assertRaises(ValueError):
            afr.Mapping(id="AF-0001", relation="kinda")


class TestCrosswalk(unittest.TestCase):
    def test_exact_mapping(self):
        hits = afr.map("agentrx", "Invalid Invocation")
        self.assertEqual([(h.id, h.relation) for h in hits], [("AF-0023", "exact")])

    def test_one_to_many(self):
        hits = afr.map("agentrx", "System Failure")
        self.assertEqual(len(hits), 3)
        self.assertTrue(all(h.relation == "narrower" for h in hits))

    def test_deliberately_unmapped(self):
        self.assertEqual(afr.map("agentrx", "Inconclusive"), [])
        self.assertEqual(afr.map("agent-xray", "valid_alternative_path"), [])

    def test_unknown_category_is_quiet_by_default(self):
        self.assertEqual(afr.map("agentrx", "Nonexistent"), [])

    def test_unknown_category_strict(self):
        with self.assertRaises(KeyError):
            afr.map("agentrx", "Nonexistent", strict=True)

    def test_roundtrip_inverts_relation(self):
        # AgentRx "System Failure" is broader than AF-0064.
        forward = [h for h in afr.map("agentrx", "System Failure") if h.id == "AF-0064"]
        self.assertEqual(forward[0].relation, "narrower")
        back = [h for h in afr.unmap("AF-0064", "agentrx")]
        self.assertEqual(back[0].relation, "broader")

    def test_unmap_across_sources(self):
        hits = afr.unmap("AF-0064", "agent-xray")
        cats = {h.category for h in hits}
        self.assertEqual(cats, {"context_overflow", "memory_overload"})

    def test_registry_only_gap(self):
        # AF-0142 is the mode no existing taxonomy names.
        for src in afr.sources():
            self.assertEqual(afr.unmap("AF-0142", src.id), [])

    def test_coverage(self):
        c = afr.coverage("agent-xray")
        self.assertEqual(c["categories"], 22)
        self.assertIn("tool_bug", c["unmapped"])


class TestNormalizeAndProfile(unittest.TestCase):
    def test_normalize_counts_dict(self):
        labels = afr.normalize({"stuck_loop": 5, "timeout": 2}, "agent-xray")
        self.assertEqual(labels[0].category, "stuck_loop")
        self.assertEqual(labels[0].count, 5)
        self.assertEqual(labels[0].best.id, "AF-0058")

    def test_normalize_iterable(self):
        labels = afr.normalize(["timeout", "timeout", "early_abort"], "agent-xray")
        by_cat = {l.category: l.count for l in labels}
        self.assertEqual(by_cat, {"timeout": 2, "early_abort": 1})

    def test_best_prefers_exact(self):
        labels = afr.normalize({"tool_selection_bug": 1}, "agent-xray")
        self.assertEqual(labels[0].best.relation, "overlaps")
        labels = afr.normalize({"context_overflow": 1}, "agent-xray")
        self.assertEqual(labels[0].best.relation, "exact")

    def test_profile_totals(self):
        p = afr.profile(afr.normalize(
            {"stuck_loop": 6, "timeout": 3, "unclassified": 1}, "agent-xray"))
        self.assertEqual(p.total, 10)
        self.assertEqual(p.by_mode["AF-0058"], 6)
        self.assertEqual(p.unmapped_total, 1)

    def test_profile_layers(self):
        p = afr.profile(afr.normalize(
            {"stuck_loop": 6, "timeout": 3}, "agent-xray"))
        self.assertEqual(p.by_layer, {"harness": 6, "environment": 3})

    def test_no_double_counting_on_multi_map(self):
        # "System Failure" maps to three modes; it must count once.
        p = afr.profile(afr.normalize({"System Failure": 4}, "agentrx"))
        self.assertEqual(p.total, 4)
        self.assertEqual(sum(p.by_mode.values()), 4)

    def test_render_is_stable(self):
        p = afr.profile(afr.normalize({"stuck_loop": 1}, "agent-xray"))
        out = p.render()
        self.assertIn("AF-0058", out)
        self.assertIn("failure profile", out)

    def test_empty_profile(self):
        self.assertEqual(afr.profile([]).render(), "no labels")


if __name__ == "__main__":
    unittest.main(verbosity=2)
