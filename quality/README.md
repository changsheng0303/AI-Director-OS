# Quality and Failure Memory

`failure-registry.jsonl` stores evidence-backed production failures and their repair status.

Validate and summarize:

```powershell
python "skills/short-drama-system/scripts/validate_failure_registry.py" "quality/failure-registry.jsonl" --summary
```

Rules:

- record observed evidence, not imagined model behavior;
- distinguish source logic, validator failures, user feedback, and actual generation outputs;
- actual generation failures require an artifact path;
- repair the current project first;
- do not promote one aesthetic preference or one model failure into a global rule;
- promote repeated failures only with cross-project evidence and a regression fixture.
