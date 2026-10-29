"""Run manually to capture evidence of a deliberately failing check.
This is intentionally NOT part of the normal pytest suite or CI workflow.
"""
print("Intentional failure demonstration: expected result is FAIL (exit code 1).")
raise SystemExit(1)
