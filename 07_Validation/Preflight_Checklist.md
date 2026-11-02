# Rehearsal and validation checklist

- [ ] Fabric workspace and Lakehouse exist with correct permissions/capacity.
- [ ] All six base CSVs uploaded to `Files/ignite_data/`.
- [ ] `01_fabric_notebook_setup.py` succeeds and creates six Delta tables and empty `new_evidence`.
- [ ] `03_validation_sql.sql` confirms 2025 £981,000, 2026 £585,000, change −40.37% (or investigate mismatch).
- [ ] Fabric Data Agent has correct source and can answer revenue and stock questions.
- [ ] Data Agent published; supported Fabric IQ tool available and Foundry connected with working identity.
- [ ] Foundry tool invocation returns actual Fabric-backed evidence; trace can be opened.
- [ ] Operational data is used in Foundry investigation, not only sales and inventory.
- [ ] `new_evidence` initially has zero rows; reveal script inserts expected records once.
- [ ] After reveal, Data Agent/Foundry can access new rows; otherwise adjust demo plan honestly.
- [ ] Run at least 3 evaluation cases: revenue arithmetic, unsupported causality, new-evidence visibility.
- [ ] Demonstrate permission boundary with an authorised test identity; do not expose secrets.
- [ ] Demonstrate a real or clearly labelled manual human-review decision.
- [ ] Rehearse 25 minutes and keep a clearly labelled recorded backup.
