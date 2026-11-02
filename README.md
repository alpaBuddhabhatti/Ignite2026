# Ignite 2026 — From Data to Decisions

**Session:** *From Data to Decisions: Fabric Data Agent Meets Microsoft Foundry* (25 minutes)

Retail investigation demo: a UK retailer's electronics revenue fell **−40.4%**
(£981,000 → £585,000, Sep 2025 → Sep 2026). Management blames inventory. The demo uses
**Microsoft Fabric Data Agent** and **Microsoft Foundry** to test that assumption,
uncover a second cause (promotion cuts), and reveal staged audit evidence — ending in
human-reviewed recommendations.

## Repository layout

| Folder | Contents |
|---|---|
| [01_Presentation](./01_Presentation) | Audience-facing slide deck |
| [02_Speaker_Notes](./02_Speaker_Notes) | Full 25-minute speaker transcript |
| [03_First_Time_Setup](./03_First_Time_Setup) | Beginner Fabric + Foundry setup guide |
| [04_Use_Case](./04_Use_Case) | Retail business use case |
| [05_Demo_Solution](./05_Demo_Solution) | Implementation kit: data, notebook sources, agent instructions, demo prompts |
| [06_On_Stage_Runbook](./06_On_Stage_Runbook) | What to show and when |
| [07_Validation](./07_Validation) | Pre-flight checklist |
| [08_Deployed_Fabric_Notebooks](./08_Deployed_Fabric_Notebooks) | **As-deployed** notebook exports from the Fabric workspace (with fixes) |
| [From_Data_to_Decisions_Ignite2026.pptx](./From_Data_to_Decisions_Ignite2026.pptx) | Alternate 9-slide deck with full speaker script in slide notes |

Start with [START_HERE.md](./START_HERE.md).

## Deployment status (Fabric workspace `Ignite2026`)

Deployed and verified on 2026-11-02:

- ✅ `RetailLakehouse` — 7 CSVs loaded, 7 Delta tables created
- ✅ Ground truth validated in-Lakehouse (`03_validation_sql`): −40.37%, low stock = S01–S04 only, 2026 promo spend kept only in S01–S03
- ✅ **`RetailEvidence` Data Agent** created, configured, **published** (all 7 tables selected)
- ✅ Demo 1 prompts 1–3 smoke-tested — on-script answers incl. the correlation ≠ causation caveat
- ✅ Formal evaluation ([evaluate_data_agent](https://learn.microsoft.com/en-us/fabric/data-science/evaluate-data-agent)) — **5/5 TRUE**, results in `demo_eval` Delta table

### Notes & gotchas

- The SDK's `datasource.select("dbo", table)` silently selects nothing on this Lakehouse
  (element tree starts with a `Schemas` grouping node). `04_create_data_agent` uses
  select-all instead.
- Keep `new_evidence` at **0 rows** before the live reveal — run `05_reset_demo3`
  after every Demo 3 rehearsal.
- Demo 3 is a **manual batch append**, not real-time streaming — never call it streaming.

### Remaining manual steps

1. Foundry agent with **Fabric IQ** tool attached to the published Data Agent
   (`05_Demo_Solution/.../05_foundry_agent_instructions.txt`).
2. Full stage rehearsal per `07_Validation/Preflight_Checklist.md`.


