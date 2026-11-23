---
title: Ignite 2026 Fabric and Foundry Lab Guide
description: Hands-on setup, implementation, permissions, testing, and local Streamlit steps for the synthetic retail investigation lab
ms.date: 2026-11-22
ms.topic: tutorial
keywords:
  - Microsoft Fabric
  - Microsoft Foundry
  - Fabric Data Agent
  - Fabric IQ
  - Streamlit
---

## Lab overview

Build a synthetic retail investigation using a Fabric Lakehouse, a published
Fabric Data Agent, a Microsoft Foundry agent connected through Fabric IQ, and
an optional local Streamlit client. The lab starts with six CSV files and adds
three audit observations through a separate manual batch append.

Follow the numbered setup, implementation, and validation steps in order.

The lab uses sample data only. It does not create a production data workflow or
execute business actions. Fabric IQ is a preview feature, and its behavior,
availability, and user interface can change. Review the current Microsoft
documentation and your organization's approval requirements before connecting
data.

## Learning outcomes

By completing the lab, you will:

* Create or access a Fabric workspace and Lakehouse.
* Load the sample files and create Delta tables with the supplied notebook.
* Validate the synthetic revenue results with SQL.
* Publish a Fabric Data Agent over selected Lakehouse tables.
* Connect a Foundry agent to the published data agent through Fabric IQ.
* Verify actual Fabric tool calls and distinguish evidence from hypotheses.
* Run the optional local Streamlit app against a Foundry agent.

## Lab assets

Use the implementation files already in this repository:

* [Retail solution overview](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/README_START_HERE.md)
* [Synthetic CSV data](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/data/)
* [Fabric table setup notebook source](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/01_fabric_notebook_setup.py)
* [Manual evidence append notebook source](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/02_reveal_new_evidence.py)
* [SQL validation queries](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/03_validation_sql.sql)
* [Fabric Data Agent instructions](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/04b_fabric_data_agent_instructions_code_interpreter.txt)
* [Foundry agent instructions](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/05b_foundry_agent_instructions_code_interpreter.txt)
* [Example prompts](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/06_demo_prompts.txt)

The linked Fabric assets are included in this repository. Foundry provisioning
templates, deployment scripts, and Streamlit application source are not included
in this attendee-guide publication. Use the portal instructions below for
Foundry, and ask the lab administrator for a separately approved application
package if you want to run the optional Streamlit client.

## Choose an environment path

### Use a prepared lab environment

This is the recommended path for a group lab. Ask the environment
administrator to prepare the Fabric and Foundry resources and grant each
participant the roles listed in [Permissions](#permissions). Participants
should not need subscription-wide resource-creation permissions.

### Create an isolated environment

Create resources only in an approved subscription. Generate a short unique
lab suffix, such as `k7m4`, and use it in resource names. Replace the example
suffix; do not reuse another participant's names.

| Resource | Example name |
|---|---|
| Lab suffix | `k7m4` |
| Resource group | `rg-ignite26-k7m4` |
| Foundry resource | `ignite26-k7m4-ai` |
| Foundry project | `ignite26-k7m4` |
| Fabric workspace | `ignite26-k7m4-fabric` |
| Lakehouse | `RetailInvestigationLH` |
| Fabric Data Agent | `RetailEvidence-k7m4` |
| Foundry agent | `RetailDecisionAdvisor-k7m4` |
| Model deployment | `gpt-5-mini-k7m4` |

Choose a supported Azure region for the Foundry resource and model. Choose a
Fabric workspace region supported by Fabric Data Agent and Fabric IQ; the Data
Agent and its data sources must meet Microsoft's current regional requirements.
An authorized administrator may need to create the resource group, Foundry
resource, and Fabric workspace or assign Fabric capacity. Follow the
resource-creation steps in [Lab 3](#lab-3-create-the-foundry-project-and-agent)
and ask administrators to grant the roles in [Permissions](#permissions).

Use the portal steps in this guide or an infrastructure template approved by
your administrator. Verify resource names, model availability, role assignments,
and costs before provisioning. The
[Foundry model catalog documentation](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)
lists supported models, but availability, versions, deployment types, and quota
vary by region and subscription.

## Prerequisites

### Accounts and services

* A Microsoft Entra account that can access both Fabric and Foundry. Use the
  same account and tenant for both services. If your organization uses a guest
  identity, the invitation must be accepted in the resource tenant.
* A Fabric capacity of F2 or higher, or an eligible Power BI Premium capacity
  with Fabric enabled. Place the workspace in a region that supports Fabric
  Data Agent and Fabric IQ.
* A Fabric tenant administrator who can enable the applicable Data Agent and
  cross-geo AI settings when organizational policy requires them.
* An Azure subscription and a Foundry project with a deployed model.
* An approved model deployment with available regional quota.
* Python 3.10 or later for the optional Streamlit application.
* Azure Developer CLI (azd) authentication for the optional local application
  and the supplied Foundry scripts.

### Permissions

Have the appropriate administrators assign access at the narrowest supported
scope. A subscription-wide Owner role is not required for every participant.

| Activity | Access to arrange |
|---|---|
| Create the Foundry account, project, or model deployment | An authorized Azure or Foundry resource owner must provision the resources. The person deploying infrastructure also needs permission to create any included role assignments. |
| Create and run Fabric notebooks | A Fabric workspace role that allows item creation and execution, plus write access to the lab Lakehouse. Ask the Fabric workspace administrator to grant the minimum role needed. |
| Create and publish the Fabric Data Agent | Permission to create and publish the agent in the workspace, and read access to the Lakehouse tables used by the agent. |
| Build and test a Foundry agent | **Foundry User** on the Foundry project for the developer identity. The project managed identity also needs the applicable Foundry access. |
| Configure the Foundry-to-Fabric IQ connection | **Foundry Project Manager** on the project, or an administrator who can create the connection. |
| Invoke an existing Foundry agent only | A least-privilege agent-consumer role supported by the project and API. Do not grant authoring roles solely to send requests. |
| Query through the Fabric Data Agent | A Fabric license and read access to the published Data Agent and its underlying Lakehouse data for the identity used by the connection. |

Foundry role names may appear under older Azure AI names in some interfaces
while renaming rolls out. Confirm current role names and scopes in the official
[Foundry RBAC documentation](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

Fabric IQ uses the configured connection identity and enforces that identity's
Fabric permissions. The Data Agent and its sources must be accessible to that
identity. The Foundry project and Fabric workspace must meet current tenant and
region requirements.

## Cost and data-handling checks

* Fabric capacity and Foundry model usage can have separate billing scopes.
  Confirm budgets and expected charges with the resource owner.
* Use only the synthetic files in this repository. Do not upload personal,
  confidential, or production data.
* Fabric IQ is a preview. Microsoft documents that data returned by Fabric can
  be processed by Foundry outside the Fabric compliance boundary or geographic
  region. Obtain required organizational approval before connecting data.
* Do not place access tokens, client secrets, API keys, or passwords in source
  files, prompts, screenshots, or shared environment files.

## Lab 1: Prepare the Fabric Lakehouse

1. Sign in to the [Microsoft Fabric portal](https://app.fabric.microsoft.com)
   with the account that has access to the target tenant.
2. Open the prepared lab workspace, or create a new workspace on the approved
   paid capacity and in a supported region.
3. Create a Lakehouse for this lab. Use an isolated Lakehouse because the setup
   notebook overwrites tables with matching names.
4. In the Lakehouse, create `Files/ignite_data`.
5. Upload these six files from the solution's `data` folder:

   * `dim_store.csv`
   * `dim_product.csv`
   * `fact_daily_sales.csv`
   * `fact_inventory.csv`
   * `fact_promotion.csv`
   * `fact_store_operations.csv`

6. Do not upload `new_evidence_reveal.csv` yet.
7. Create a Fabric notebook, attach the lab Lakehouse as its default Lakehouse,
   and copy the full contents of
   [the setup notebook source](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/01_fabric_notebook_setup.py)
   into a Python cell.
8. Run the cell. Confirm it creates the six base Delta tables and an empty
   `new_evidence` table.
9. In the Lakehouse SQL analytics endpoint, run the queries in
   [the validation SQL file](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/03_validation_sql.sql).
10. Check the low-stock store set and distinct store count:

    ```sql
    SELECT DISTINCT StoreId
    FROM fact_inventory
    WHERE IsLowStock = 1
      AND SnapshotDate = (SELECT MAX(SnapshotDate) FROM fact_inventory)
    ORDER BY StoreId;

    SELECT SnapshotDate, COUNT(DISTINCT StoreId) AS LowStockStoreCount
    FROM fact_inventory
    WHERE IsLowStock = 1
      AND SnapshotDate = (SELECT MAX(SnapshotDate) FROM fact_inventory)
    GROUP BY SnapshotDate;
    ```

    The supplied synthetic snapshot should identify four stores, `S01` through
    `S04`, on `2026-09-15`. This is a snapshot observation, not proof of a
    month-long shortage.

The setup notebook uses overwrite mode. Run it only against a disposable lab
Lakehouse. Do not use it to reset a shared Lakehouse or any environment
containing data you need to preserve.

## Lab 2: Create and validate the Fabric Data Agent

The Data Agent is a Fabric workspace item configured in the portal. The
repository supplies its instruction text and source data, not a standalone
Data Agent application to deploy.

1. In the lab workspace, create a Fabric Data Agent.
2. Add the lab Lakehouse and select these tables:

   * `dim_store`
   * `dim_product`
   * `fact_daily_sales`
   * `fact_inventory`
   * `fact_promotion`
   * `fact_store_operations`
   * `new_evidence`

3. Copy the contents of
   [the Fabric Data Agent instructions](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/04b_fabric_data_agent_instructions_code_interpreter.txt)
   into its instructions.
4. Test the agent with this question:

   ```text
   Compare Electronics revenue for September 2025 and September 2026. Return
   both totals, the GBP change, the percentage change, and the source tables.
   Use Revenue, not Units.
   ```

5. Verify the result against SQL: £981,000 for September 2025 and £585,000 for
   September 2026. The change is -£396,000, or approximately -40.4%.
6. Confirm the answer identifies `fact_daily_sales` and `dim_product`, and does
   not claim the revenue decline proves a cause.
7. Test inventory with:

   ```text
   Which distinct stores have IsLowStock set in the latest inventory snapshot?
   Give the store IDs, distinct-store count, snapshot date, and source table.
   Do not describe the snapshot as proof of a sustained shortage.
   ```

   Verify the result against SQL: four distinct stores, `S01` through `S04`,
   on `2026-09-15`, from `fact_inventory`.
8. Publish the Data Agent. A draft agent is not available in the Foundry
   OneLake Catalog.

If the agent is unavailable in the catalog, verify publication, workspace
access, source permissions, capacity, tenant settings, region, and account
selection.

## Lab 3: Create the Foundry project and agent

### Prepare the project

1. In the [Azure portal](https://portal.azure.com), select the approved
   subscription and create the example resource group from the naming table,
   such as `rg-ignite26-k7m4`. If the `Microsoft.CognitiveServices` resource
   provider is not registered, ask an administrator to register it.
2. Create a Microsoft Foundry resource in that resource group. Use the example
   unique name `ignite26-k7m4-ai`, an approved region, and the organization's
   required networking and security settings. Resource type and SKU labels can
   differ as the Foundry portal evolves; use a resource type currently
   documented for Foundry projects.
3. Open the [Microsoft Foundry portal](https://ai.azure.com), create a project
   named `ignite26-k7m4`, and select the resource created in the previous step.
   The portal may also let an authorized project creator create the resource
   during project setup.
4. Open the project's model catalog and deploy **GPT-5 mini**
   (`gpt-5-mini`) if it is available in the region and supported by Agent
   Service. Use `gpt-5-mini-k7m4` as the deployment name, or record the name
   assigned by the portal. If unavailable, select a model that the project
   catalog lists as supported and use its deployment consistently. Check quota
   and costs before deploying or sending requests.
5. Ask the administrator to assign **Foundry User** to the agent developer and
   project managed identity, and **Foundry Project Manager** to the identity
   that configures the Fabric IQ connection. Do not assign resource-creation
   roles to every attendee.
6. If an administrator provisions the resources for you, confirm the resource,
   project, deployment, and role-assignment names before continuing.

### Add the Fabric Data Agent through Fabric IQ

1. Create a new prompt agent in the project.
2. Name it `RetailDecisionAdvisor-<suffix>` and select the model deployment
   created in the previous step.
3. In **Tools**, select **Add** and browse for **Fabric IQ (OneLake Catalog)**.
4. Filter the catalog to **Data agent**, select the published
   `RetailEvidence-<suffix>` Data Agent, and add it. Complete the Fabric IQ
   connection flow using an identity with **Foundry Project Manager** and the
   required Fabric read permissions.
5. If the task requires calculations or charts from retrieved results, add
   **Code Interpreter** as an additional tool. Code Interpreter is not a
   connection to Fabric; it can process only values returned by the Fabric
   tool.
6. Copy the contents of
   [the Foundry agent instructions](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/05b_foundry_agent_instructions_code_interpreter.txt)
   into the agent instructions.
7. Save the agent and test it in the Foundry Playground.
8. Confirm the run history shows a call to the Fabric IQ Data Agent for a
   business-data question. Ask which stores are low on stock and verify that
   the response reports `S01` through `S04` as a snapshot observation. If you
   added Code Interpreter, test a calculation using values returned by Fabric
   and confirm the run history shows that tool call too.

This guide uses the Foundry portal for agent creation. If your lab administrator
provides deployment code, confirm that it is approved for your project and
region. Do not reuse scripts or identifiers from another environment without
review.

### Verify the Foundry integration

1. In the Foundry Playground, submit:

   ```text
   Use the connected Fabric Data Agent to compare Electronics revenue for
   September 2025 and September 2026. Return both totals, the GBP and percentage
   change, and the source tables. If the Fabric tool cannot be queried, say so;
   do not guess.
   ```

2. Inspect tool activity or Foundry Traces. Confirm an actual Fabric Data
   Agent invocation and returned evidence. Seeing the tool in a list is not
   proof that it ran.
3. Ask the agent to calculate the change from the retrieved totals. If you
   enabled Code Interpreter, verify that it actually ran and used only those
   returned values.
4. Ask a follow-up that compares inventory, promotion, and store operations.
   Confirm the response labels observed data, hypotheses, and missing evidence
   separately.
5. Confirm proposed actions remain proposals and the agent does not claim to
   execute or approve them.

## Lab 4: Reveal and validate the additional evidence

1. Confirm `new_evidence` contains zero rows using the SQL analytics endpoint.
2. Upload `new_evidence_reveal.csv` to `Files/ignite_data`.
3. Create a second notebook attached to the same lab Lakehouse.
4. Copy the full contents of
   [the reveal notebook source](../05_Demo_Solution/Fabric_Retail_Decisions_No_Eventhouse/02_reveal_new_evidence.py)
   into a Python cell.
5. Run the cell once. It checks for exactly three source rows and appends them
   to `new_evidence`.
6. Refresh the SQL endpoint and verify that `new_evidence` contains three rows.
   Allow for endpoint refresh delay before troubleshooting.
7. Ask the Fabric Data Agent or Foundry agent to query `new_evidence`. Confirm
   the response describes the three observations and does not infer a
   month-long inventory shortage from a single snapshot.

The append is not idempotent. Running it more than once can duplicate the
records. To reset a disposable lab, run the
[reset notebook](../08_Deployed_Fabric_Notebooks/05_reset_demo3.Notebook/notebook-content.ipynb)
and verify that `new_evidence` returns to zero rows. Do not rerun the setup
notebook to reset this table because it overwrites the base tables.

## Lab 5: Test the end-to-end investigation

1. In the Foundry Playground, ask the agent to compare the two September
   Electronics revenue totals. Verify the values against the SQL results and
   confirm the agent names the source tables.
2. Ask the agent:

   ```text
   Use the connected Fabric Data Agent to summarize all three rows in
   new_evidence. Include the observation dates and sources. Explain what these
   observations establish and what they do not prove.
   ```

3. Confirm the answer includes all three observations from `new_evidence` and
   does not infer a sustained inventory shortage from a single snapshot.
4. Inspect the Foundry run history or traces. Confirm the request actually
   invoked the Fabric Data Agent and used its returned evidence.
5. If you enabled Code Interpreter, ask the agent to calculate a value from the
   returned data and confirm the run history shows that tool call.

## Lab 6: Run the optional Streamlit application locally

The Streamlit application source is not included in this GitHub guide
publication. Ask the lab administrator for the approved app package before
starting this lab. The client calls Foundry with an Azure Developer CLI access
token; it does not store a model key or supply retail facts.

1. Install Python 3.10 or later and Azure Developer CLI.
2. Open PowerShell in the folder containing the application package supplied by
   the lab administrator.
3. Create and activate a virtual environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the packages:

   ```powershell
   python -m pip install -r .\requirements.txt
   ```

5. Set the project endpoint, agent name, and version for the environment you
   will use. The application reads `FOUNDRY_PROJECT_ENDPOINT`,
   `FOUNDRY_AGENT_NAME`, and `FOUNDRY_AGENT_VERSION`. Set process-scoped
   PowerShell environment variables before launching the application. Do not
   put credentials in these values.

   For example, in the same PowerShell window:

   ```powershell
   $env:FOUNDRY_PROJECT_ENDPOINT = "https://<resource>.services.ai.azure.com/api/projects/<project>"
   $env:FOUNDRY_AGENT_NAME = "<agent-name>"
   $env:FOUNDRY_AGENT_VERSION = "<version>"
   ```

6. Authenticate to the correct tenant:

   ```powershell
   azd auth login --tenant-id <your-tenant-id>
   ```

7. Start the app from the same activated PowerShell session:

   ```powershell
   python -m streamlit run .\streamlit_app.py
   ```

8. Open [http://127.0.0.1:8501](http://127.0.0.1:8501). Submit a quick prompt
   and confirm a Foundry response is returned. Use **Reset conversation**
   before repeating tests.
9. Stop Streamlit with `Ctrl+C`.

Do not store secrets in a local `.env` file or commit local environment files.
Use Azure Developer CLI sign-in and process-scoped settings instead.

## Validation checklist

* [ ] The Fabric workspace uses the approved capacity and supported region.
* [ ] The Lakehouse contains the six base tables and an empty `new_evidence`
  table before the reveal.
* [ ] SQL returns £981,000 and £585,000 for the two September periods, a
  -£396,000 change, and approximately -40.4%.
* [ ] The published Fabric Data Agent returns the same results and cites the
  expected source tables.
* [ ] The Foundry request includes an actual Fabric tool invocation and uses
  returned evidence rather than guessed values.
* [ ] The Foundry response distinguishes evidence from hypotheses and does not
  claim to execute a business action.
* [ ] The reveal appends three records exactly once, and the reset returns the
  table to zero rows.
* [ ] The Foundry run history confirms actual Fabric tool calls and returned
  evidence.
* [ ] If the optional Streamlit package is provided, the application
  authenticates, responds, and resets its conversation.
* [ ] No tokens, credentials, personal data, or unreviewed response artifacts
  are included in files shared with others.

## Troubleshooting

| Symptom | Checks |
|---|---|
| CSV is not found | Confirm the Lakehouse default attachment and exact `Files/ignite_data` paths. |
| SQL returns no tables | Confirm the setup cell completed, the notebook is attached to the intended Lakehouse, and the SQL endpoint has refreshed. |
| Revenue differs | Re-run the supplied SQL; check the September filters, Electronics category join, and `SUM(Revenue)` rather than `SUM(Units)`. |
| Data Agent is missing from OneLake Catalog | Confirm it is published, the signed-in identity can access it and the Lakehouse, and tenant, capacity, region, and account requirements are met. |
| Foundry does not call Fabric | Confirm the Fabric IQ tool is attached, the agent instructions name the Data Agent, the user has Fabric read access, and tool activity shows an invocation. |
| Foundry connection cannot be created | Ask a project administrator to verify the **Foundry Project Manager** assignment and connection consent. |
| Streamlit authentication fails | Sign in to the correct tenant with Azure Developer CLI and confirm the account can invoke the configured Foundry agent. |
| Evidence appears more than once | Reset the disposable lab table, verify zero rows, then run the append cell once. |

## Official documentation

* [Create a Fabric Data Agent](https://learn.microsoft.com/fabric/data-science/how-to-create-data-agent)
* [Connect a Foundry agent to Fabric through Fabric IQ](https://learn.microsoft.com/fabric/data-science/data-agent-foundry-fabric-iq)
* [Fabric IQ tool requirements and configuration](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric-iq)
* [Create a Foundry project](https://learn.microsoft.com/azure/foundry/how-to/create-projects)
* [Role-based access control for Microsoft Foundry](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry)
* [Fabric Data Agent tenant settings](https://learn.microsoft.com/fabric/data-science/data-agent-tenant-settings)
