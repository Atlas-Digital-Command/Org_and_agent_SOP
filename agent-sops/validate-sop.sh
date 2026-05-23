#!/usr/bin/env bash
# validate-sop.sh — verify a .sop.md or generated SOP file matches the framework's format spec.
#
# Usage:
#   ./validate-sop.sh path/to/file.sop.md
#   ./validate-sop.sh path/to/generated-sop.md
#
# Exit codes:
#   0  All checks passed
#   1  One or more errors found
#   2  Bad invocation (missing file, wrong arguments)
#
# Output legend:
#   PASS  required check satisfied
#   WARN  recommended check failed (non-blocking)
#   FAIL  required check failed (blocking)

set -u

# ----- argument parsing -----

if [[ $# -ne 1 ]]; then
  printf 'usage: %s <path-to-sop>\n' "$0" >&2
  exit 2
fi

SOP_PATH="$1"

if [[ ! -f "$SOP_PATH" ]]; then
  printf 'error: file not found: %s\n' "$SOP_PATH" >&2
  exit 2
fi

# ----- counters -----

ERRORS=0
WARNINGS=0
PASSES=0

# ----- helpers -----

pass() {
  printf '  PASS  %s\n' "$1"
  PASSES=$((PASSES + 1))
}

warn() {
  printf '  WARN  %s\n' "$1"
  WARNINGS=$((WARNINGS + 1))
}

fail() {
  printf '  FAIL  %s\n' "$1"
  ERRORS=$((ERRORS + 1))
}

# Returns 0 if the file contains a line matching the given regex.
has_line() {
  grep -Eq "$1" "$SOP_PATH"
}

# Returns count of lines matching the given regex.
count_lines() {
  grep -Ec "$1" "$SOP_PATH"
}

# ----- detect SOP type -----

SOP_TYPE="unknown"
if [[ "$SOP_PATH" == *.sop.md ]]; then
  SOP_TYPE="meta"
elif [[ "$SOP_PATH" == *.md ]]; then
  if has_line '^## (Purpose|Definition of Done|Process steps?)'; then
    SOP_TYPE="generated"
  fi
fi

printf 'Validating %s\n' "$SOP_PATH"
printf 'Detected type: %s\n\n' "$SOP_TYPE"

# ----- shared checks (apply to both meta and generated SOPs) -----

printf 'Shared checks:\n'

# Title (H1) must be the first non-empty line
first_line="$(grep -m1 -E '\S' "$SOP_PATH" || true)"
if [[ "$first_line" =~ ^#\ .+ ]]; then
  pass "file begins with an H1 title"
else
  fail "file must begin with an H1 title (e.g., '# My SOP')"
fi

# UTF-8 sanity
if file "$SOP_PATH" 2>/dev/null | grep -qiE 'utf-?8|ascii'; then
  pass "file is UTF-8 / ASCII"
else
  warn "file may not be UTF-8; check encoding"
fi

# No tabs (markdown convention)
if grep -qP '\t' "$SOP_PATH"; then
  warn "file contains tab characters; spaces are preferred"
else
  pass "no tab characters"
fi

# Trailing whitespace
if grep -qE ' +$' "$SOP_PATH"; then
  warn "file contains trailing whitespace on some lines"
else
  pass "no trailing whitespace"
fi

printf '\n'

# ----- meta-SOP checks (only for .sop.md files) -----

if [[ "$SOP_TYPE" == "meta" ]]; then
  printf 'Meta-SOP (.sop.md) checks:\n'

  # Required sections per spec
  for section in 'Overview' 'Parameters' 'Steps'; do
    if has_line "^## ${section}\$"; then
      pass "has '## ${section}' section"
    else
      fail "missing required '## ${section}' section"
    fi
  done

  # Recommended sections
  for section in 'Examples' 'Troubleshooting'; do
    if has_line "^## ${section}\$"; then
      pass "has '## ${section}' section"
    else
      warn "missing recommended '## ${section}' section"
    fi
  done

  # Parameter format: -- **name** (required|optional[, default: ...]): description
  param_count=$(count_lines '^- \*\*[a-z_]+\*\* \((required|optional)')
  if [[ "$param_count" -gt 0 ]]; then
    pass "has $param_count parameter definitions in spec format"
  else
    warn "no parameters found in '- **name** (required|optional): description' format"
  fi

  # Parameter naming: snake_case only
  if grep -qE '^- \*\*[A-Z]' "$SOP_PATH" || grep -qE '^- \*\*[a-z]+-[a-z]' "$SOP_PATH"; then
    fail "parameter names must be snake_case (lowercase with underscores)"
  else
    pass "all parameter names are snake_case"
  fi

  # Required parameter acquisition constraints
  if has_line 'Constraints for parameter acquisition'; then
    pass "has 'Constraints for parameter acquisition' block"
  else
    warn "missing 'Constraints for parameter acquisition' block"
  fi

  # Steps must use '### N. Name' format
  step_count=$(count_lines '^### [0-9]+\. ')
  if [[ "$step_count" -gt 0 ]]; then
    pass "has $step_count numbered steps"
  else
    fail "no numbered steps found (expected '### 1. Step Name' format)"
  fi

  # Each step section should have a Constraints block
  steps_with_constraints=$(count_lines '\*\*Constraints:\*\*')
  if [[ "$steps_with_constraints" -ge "$step_count" ]]; then
    pass "every step has a Constraints block ($steps_with_constraints / $step_count)"
  else
    fail "some steps lack a Constraints block ($steps_with_constraints / $step_count)"
  fi

  # RFC 2119 keywords in constraints
  rfc_keywords=$(grep -cE 'You (MUST|SHOULD|MAY|MUST NOT|SHOULD NOT|SHALL NOT|REQUIRED|RECOMMENDED|OPTIONAL)' "$SOP_PATH")
  if [[ "$rfc_keywords" -gt 0 ]]; then
    pass "uses RFC 2119 keywords ($rfc_keywords occurrences)"
  else
    fail "no RFC 2119 keywords found; constraints must use MUST/SHOULD/MAY etc."
  fi

  # Negative constraints must have rationale (the word 'because', 'since', or 'as')
  # Heuristic: count negative constraint lines, then verify each contains a rationale word.
  while IFS= read -r line; do
    if [[ -n "$line" ]] && ! echo "$line" | grep -qiE 'because|since|\bas this\b|\bas the\b|\bas it\b'; then
      warn "negative constraint may lack rationale: ${line:0:90}..."
    fi
  done < <(grep -E 'You (MUST NOT|SHOULD NOT|SHALL NOT)' "$SOP_PATH" || true)

  printf '\n'
fi

# ----- generated-SOP checks (only for .md files matching the generated shape) -----

if [[ "$SOP_TYPE" == "generated" ]]; then
  printf 'Generated SOP checks:\n'

  # Minimum required sections for the leanest archetype
  for section in 'Purpose' 'Process'; do
    if has_line "^## ${section}"; then
      pass "has '## ${section}' section"
    else
      fail "missing required '## ${section}' section"
    fi
  done

  # KPIs / metrics block
  if has_line "^## (KPIs|Quality metrics|Metrics)"; then
    pass "has metrics / KPIs section"
  else
    warn "missing KPIs / Quality metrics section"
  fi

  # Definition of Done (recommended)
  if has_line "^## Definition of Done"; then
    pass "has 'Definition of Done' section"
  else
    warn "missing 'Definition of Done' section (recommended)"
  fi

  printf '\n'
fi

# ----- summary -----

printf 'Summary:\n'
printf '  %d passed\n' "$PASSES"
printf '  %d warnings\n' "$WARNINGS"
printf '  %d errors\n' "$ERRORS"

if [[ "$ERRORS" -gt 0 ]]; then
  exit 1
fi

exit 0
