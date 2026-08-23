import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import afr
from afr.model import invert


class TestModes(unittest.TestCase):
    def test_every_mode_loads(self):
        self.assertEqual(len(afr.modes()), 24)

    def test_lookup(self):
        m = afr.mode("AF-0142")
        self.assertEqual(m.title, "Stale context re-read")
        self.assertEqual(m.layer, "model")

    def test_unknown_mode_raises(self):
        with self.assertRaises(KeyError):
            afr.mode("AF-9999")

    def test_layers_are_legal(self):
        for m in afr.modes():
            self.assertIn(m.layer, afr.LAYERS)

    def test_layer_principle(self):
        # Fault lies with the component that could have acted correctly on
        # the information it had (SCHEMA, adopted 2026-08-23).
        for af_id in ("AF-0049", "AF-0058", "AF-0071", "AF-0086", "AF-0142"):
            self.assertEqual(afr.mode(af_id).layer, "model", af_id)
        self.assertEqual(afr.mode("AF-0064").layer, "harness")
        self.assertEqual(afr.mode("AF-0095").layer, "harness")

    def test_stable_modes_have_two_sources_and_an_exact(self):
        for m in afr.modes():
            if m.status != "stable":
                continue
            hits = [(s.id, e.relation) for s in afr.sources()
                    for e in (afr.unmap(m.id, s.id) or [])]
            self.assertGreaterEqual(len({s for s, _ in hits}), 2, m.id)
            self.assertIn("exact", {r for _, r in hits}, m.id)

    def test_near_neighbors_resolve(self):
        ids = {m.id for m in afr.modes()}
        for m in afr.modes():
            for nn in m.near_neighbors:
                self.assertIn(nn, ids)

    def test_near_neighbors_are_reciprocal(self):
        by_id = {m.id: m for m in afr.modes()}
        for m in afr.modes():
            for nn in m.near_neighbors:
                self.assertIn(m.id, by_id[nn].near_neighbors,
                              "%s lists %s but not vice versa" % (m.id, nn))


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

    def test_mapping_repr_is_compact(self):
        # What the README promises `afr.map()` prints at a REPL.
        self.assertEqual(repr(afr.Mapping(id="AF-0023", relation="exact")),
                         "AF-0023 (exact)")
        self.assertEqual(repr(afr.map("agentrx", "Invalid Invocation")),
                         "[AF-0023 (exact)]")

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
        self.assertEqual([h.id for h in hits], ["AF-0170", "AF-0136", "AF-0130", "AF-0149"])
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
        # AgentRx "System Failure" is broader than AF-0136.
        forward = [h for h in afr.map("agentrx", "System Failure") if h.id == "AF-0136"]
        self.assertEqual(forward[0].relation, "narrower")
        back = [h for h in afr.unmap("AF-0136", "agentrx")]
        self.assertEqual(back[0].relation, "broader")

    def test_unmap_across_sources(self):
        hits = afr.unmap("AF-0064", "agent-xray")
        cats = {h.category for h in hits}
        self.assertEqual(cats, {"context_overflow", "memory_overload"})
        self.assertEqual(len(afr.sources()), 6)

    def test_no_orphan_modes(self):
        # Every mode has at least one source. AF-0142 was the last orphan;
        # Model-or-Harness "State Tracking Failure" names re-reads as a sub-case.
        hits = afr.unmap("AF-0142", "model-or-harness")
        self.assertEqual([(h.category, h.relation) for h in hits],
                         [("State Tracking Failure", "broader")])
        for m in afr.modes():
            self.assertTrue(any(afr.unmap(m.id, s.id) for s in afr.sources()), m.id)

    def test_coverage(self):
        c = afr.coverage("agent-xray")
        self.assertEqual(c["categories"], 22)
        # tool_bug is partially covered (overlaps) but still a flagged GAP.
        self.assertNotIn("tool_bug", c["unmapped"])
        self.assertEqual(set(c["unmapped"]),
                         {"valid_alternative_path", "consultative_success", "unclassified"})

    def test_tool_layer_exists(self):
        # AF-0149 closed the registry's empty tool layer; tool_bug's best
        # mapping lands there rather than on the agent-side error modes.
        m = afr.mode("AF-0149")
        self.assertEqual(m.layer, "tool")
        labels = afr.normalize({"tool_bug": 1}, "agent-xray")
        self.assertEqual(labels[0].best.id, "AF-0149")
        self.assertEqual({h.id for h in labels[0].af}, {"AF-0149", "AF-0011", "AF-0023"})

    def test_gap_notes_survive_partial_mapping(self):
        # A category can be mapped by overlaps and still be a roadmap item.
        for src, cat in (("agent-xray", "routing_bug"), ("agentrx", "Guardrails Triggered")):
            hits = afr.map(src, cat)
            self.assertTrue(hits, cat)
            self.assertTrue(all(h.relation != "exact" for h in hits), cat)
            self.assertTrue(hits[0].note.startswith("GAP"), cat)

    def test_two_source_modes(self):
        # Each mode written from the academic read has >= 2 independent sources.
        for af_id in ("AF-0153", "AF-0157", "AF-0161", "AF-0166", "AF-0170"):
            srcs = {s.id for s in afr.sources() if afr.unmap(af_id, s.id)}
            self.assertGreaterEqual(len(srcs), 2, "%s: %s" % (af_id, srcs))
        self.assertEqual(afr.normalize({"tool_selection_bug": 1}, "agent-xray")[0].best.id, "AF-0157")
        self.assertEqual(afr.normalize({"Tool-Skip": 1}, "toolfailbench")[0].best.id, "AF-0153")


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
        labels = afr.normalize({"reasoning_bug": 1}, "agent-xray")
        self.assertEqual(labels[0].best.relation, "overlaps")
        labels = afr.normalize({"spin": 1}, "agent-xray")
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
        self.assertEqual(p.by_layer, {"model": 6, "environment": 3})

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
