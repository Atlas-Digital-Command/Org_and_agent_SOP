# Examples

Reference overlay archetypes. Each subdirectory is a fully-populated, sanitized `governance/` + `org-map/` overlay that demonstrates how a different kind of organization would configure the framework.

## The three archetypes

| Folder | Archetype | When to use |
|---|---|---|
| [`lean-operator/`](./lean-operator) | Solo or small team, generalists, one decider | Defaults here — the "lowest common denominator" the framework reaches for when an org profile is ambiguous |
| [`coordinated-specialist/`](./coordinated-specialist) | Mid-size, specialized roles, departmental approvals | Most growing agencies; balances depth with efficiency |
| [`compliance-forward/`](./compliance-forward) | Larger orgs with active compliance frameworks | SOC 2, HIPAA, ISO, multi-tier approvals, formal audit trails |

The archetypes scale along a single axis:

```
Directness + Efficiency  ←————————————————————————→  Compliance + Thoroughness
   (Lean Operator)         (Coordinated Specialist)    (Compliance-Forward)
```

See the [main README](../README.md#the-three-archetypes) for the dimensional breakdown.

## Plus: Atlas-public

[`atlas-public/`](./atlas-public) holds 1-2 sanitized, real SOPs that Atlas Digital produced using this framework — included for credibility and as a working example of the output. Atlas's *full* governance + org-map remains private (loaded via overlay at runtime).

## Using an example as a starting point

```bash
# Copy whichever archetype best matches your org
cp -r examples/lean-operator ~/.sop-agent/overlay/

# Edit the files to reflect your real organization
$EDITOR ~/.sop-agent/overlay/governance/org-profile.md

# Run the agent — it auto-discovers the overlay
sop-agent new "Quarterly content audit"
```

**Coming in Phase 1:** All three archetype overlays will be fully populated with realistic governance and org-map content.
