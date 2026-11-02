# Microsoft Ignite 2026 — No-Eventhouse Retail Investigation

**Audience session:** From Data to Decisions: Fabric Data Agent Meets Microsoft Foundry.

This package is a **local implementation kit**; it does not create cloud resources. Synthetic dataset; no actual customer data. No Eventhouse, Eventstream, Event Hubs or streaming required.

## Data truth
Electronics September 2025 revenue: 981,000.00; September 2026 revenue: 585,000.00; change: -40.37%. Verify using `03_validation_sql.sql` in your own Fabric workspace.

## Suggested architecture
CSV -> Fabric Lakehouse Delta tables -> Fabric Data Agent (published) -> Fabric IQ tool -> Foundry Agent -> proposed decisions with human review.

New evidence arrives via a deliberate manual notebook append to the Lakehouse. This is a **batch update**, not streaming or continuous real-time data.

## Files
- `data/`: six initial CSVs and a seventh reveal CSV.
- `01_fabric_notebook_setup.py`: paste into a Fabric notebook to create Delta tables.
- `02_reveal_new_evidence.py`: paste into a second Fabric notebook and run at the live reveal.
- `03_validation_sql.sql`: ground-truth checks.
- `04_fabric_data_agent_instructions.txt`: paste into Fabric Data Agent instructions.
- `05_foundry_agent_instructions.txt`: paste into Foundry agent instructions.
- `06_demo_prompts.txt`: live demo prompts.
- Separate beginner guide DOCX: screenshots not included; every UI action is described.

## Key limitation
Do not call this real-time streaming. This demo uses newly appended records queried after refresh. Validate visibility and propagation timing in your tenant.
