# Outreach

The distribution strategy in full. AFR does not need an audience — it needs
three merges. Everything here is generated or drafted; nothing is sent yet.

## Sequence — do not do these in parallel

Order matters more than speed. Each yes strengthens the next ask.

| # | Target | Kind | Why this position in the order |
|---|---|---|---|
| 1 | **[Agent-Xray](https://github.com/GeeIHadAGoodTime/Agent-Xray)** | PR | Solo maintainer, 115 commits, 1 star. Most likely to reply, and genuinely pleased someone read the code. Their `tool_bug` category exposed a real gap in the registry, so the PR arrives carrying a finding rather than a request. |
| 2 | **[AgentDebugX](https://github.com/AgentDebugX/AgentDebugX)** | Issue | Academic authors, slower cycle, already have an Error Hub. Open the conversation early because it will take weeks, but ask a question rather than filing a diff. |
| 3 | **[AgentRx](https://github.com/microsoft/AgentRx)** | PR | Microsoft Research. Highest credibility, hardest yes. Go last so the PR can say *"Agent-Xray merged the equivalent file"* instead of *"please be first."* |

Approaching MSR first with zero adoption is the weakest possible version of
this ask. Resist it.

## Before sending anything

- [x] Replace `YOURNAME` in `scripts/export_mapping.py` (`REPO`) and regenerate:
      `make outreach`
- [x] Publish the AFR repo publicly — every PR links to it, and a 404 kills the ask
- [x] Drop the canonical Apache-2.0 text into `LICENSE-CODE`
- [x] Re-read each target's *current* taxonomy before sending. Agent-Xray:
      **done** — full read of `root_cause.py`/`analyzer.py` on 2026-08-23, notes in
      `registry/crosswalk/notes/agent-xray.md`, mapping corrected from it.
- [x] AgentRx: **done** — full read of `judge.py` `TAXONOMY_DATA` + checklists,
      paper §2–2.2/§3.4/§6, and both ground-truth files on 2026-08-23; notes in
      `registry/crosswalk/notes/agentrx.md`, mapping corrected from it.
- [x] `make check` green

## What each PR deliberately does not do

Every one of these would turn a plausible merge into a decline:

- no dependency, no import, no code change
- no request to adopt AF ids or alter their taxonomy
- no claim their taxonomy is deficient — mapping runs one way, onto them
- no marketing language, no roadmap, no "we're building the standard for…"

The file is inert. That is the whole reason it is mergeable.

## Judgement calls are surfaced, not buried

Each PR names the mappings that required a decision and invites correction. A
maintainer who finds a wrong `exact` you did not flag concludes the table is
sloppy. One who is *told where the soft spots are* concludes the opposite — and
that impression is the only asset the registry has.

## If all three decline

Not fatal, but it is real information: it means the crosswalk has no natural
home in other people's repos, and the registry has to earn attention on its own,
which is much harder. In that case publish the mappings upstream anyway, then
reconsider whether the OpenTelemetry `semantic-conventions-genai` group is the
better venue — GenAI conventions are still in Development with nothing marked
Stable, and a failure-mode attribute is squarely in scope. That is a slower,
committee-shaped path, and worth trying only once the direct route has failed.

## After a merge

Add the target to the README status line and open the reciprocal issue on AFR
recording anything their taxonomy exposed — like `tool_bug`. Contributors who
see their input change the registry contribute again.
