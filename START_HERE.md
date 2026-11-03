# START HERE — Ignite 2026 all-in-one package

Session: **From Data to Decisions: Fabric Data Agent Meets Microsoft Foundry** (25 minutes)

## Read in this order
1. `04_Use_Case/Retail_Business_Use_Case.docx` — story and exact original abstract.
2. `03_First_Time_Setup/Beginner_Fabric_Foundry_Setup_Guide.docx` — first-time deployment guide.
3. `05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/README_START_HERE.md` — implementation code and data.
4. `07_Validation/Preflight_Checklist.md` — prove each stage works before presenting.
5. `02_Speaker_Notes/Full_25_Minute_Speaker_Transcript.docx` — what to say.
6. `06_On_Stage_Runbook/What_To_Show_And_When.docx` — where to click and what the audience sees.
7. `01_Presentation/From_Data_to_Decisions_Ignite_2026.pptx` — **audience-facing slides only**.

## 25-minute timed agenda

| Time | Segment | On-stage action |
|---|---|---|
| 0:00–1:00 | Fabric in one minute | Explain that Fabric holds the governed Lakehouse data and the published `RetailEvidence` Data Agent answers questions over it. |
| 1:00–2:00 | Foundry in one minute | Explain that the Foundry agent uses tools to ground its analysis; it does not replace the data source. |
| 2:00–4:00 | Use case | Set up the retailer's question: Electronics revenue fell from £981K to £585K. Is inventory really the cause? |
| 4:00–5:00 | Architecture and tools | Show the flow: Lakehouse tables -> `RetailEvidence` -> Fabric IQ tool in the Foundry toolbox -> `Retail-Decision-Advisor` -> decision brief. |
| 5:00–10:00 | Demo 1: Fabric alone | In the Fabric Data Agent, compare September revenue, rank store declines, and inspect the inventory snapshot. |
| 10:00–15:00 | Demo 2: Foundry + Fabric | In Foundry, run the fast smoke prompt, confirm a real `RetailEvidence` call in Traces, then ask for the wider investigation. |
| 15:00–20:00 | Demo 3: new evidence | Run the prepared batch append, query `new_evidence`, and ask Foundry to revise its brief. This is a batch update, not streaming. |
| 20:00–22:00 | Decisions and guardrails | Review proposed actions, state that human approval is required, and distinguish evidence from hypotheses. |
| 22:00–24:00 | Enterprise takeaways | Cover permissions, evidence limits, and why the demo uses synthetic data and no real-time stream. |
| 24:00–25:00 | Close | Recap the data-to-decision flow and end with the audience takeaway. |

Keep the one-minute Fabric and Foundry introductions conceptual. Use the later demo slots to show each product working.

## Tool integration

The live integration uses three distinct roles:

1. **Fabric Data Agent (`RetailEvidence`)** queries the published Lakehouse tables and is the source of retail facts.
2. **Fabric IQ** is the tool connection in `Retail-Decision-Advisor-toolbox` v3 that lets Foundry call `RetailEvidence`.
3. **Foundry (`Retail-Decision-Advisor` v3)** asks the data question, interprets returned evidence, and drafts the decision brief.

Code Interpreter is optional. It can calculate changes or chart values already returned by Fabric; it is not the Fabric connector and must not invent or retrieve business data.

### Integration check before the session

- Sign in to the `MVPsOnFabric` tenant.
- Confirm `RetailEvidence` is published with the required retail tables selected.
- Confirm Foundry agent version 3 uses toolbox version 3 with the Fabric IQ `RetailEvidence` tool.
- Run one direct Fabric query, then one Foundry integration prompt.
- In Foundry Traces, confirm an actual `RetailEvidence` invocation and returned result. `mcp_list_tools` alone only lists available tools.
- Keep `new_evidence` out of the first integrated investigation; query it during the planned reveal.

## Important
- No Eventhouse, Eventstream, Event Hubs or streaming.
- Data is synthetic. Headline is ~−40.4%, verify after import.
- The third demo is a manual batch append, **not real-time streaming**.
- Foundry/Fabric IQ compatibility, permissions, tracing and refresh latency must be tested in your tenant.
- The package is a complete local kit, not a deployed cloud solution. A human-approval interaction is a demo checkpoint, not an implemented business workflow unless you build one.
