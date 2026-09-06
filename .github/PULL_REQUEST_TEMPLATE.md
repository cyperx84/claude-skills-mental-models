## Summary

<!-- What does this PR change and why? -->

## Type

- [ ] New mental model
- [ ] Edit to existing model
- [ ] Skill instructions (SKILL.md / CATALOG.md / REFERENCE.md)
- [ ] Docs
- [ ] Plugin manifests

## Checklist

- [ ] All required sections present: Description, When to Avoid, Keywords, Thinking Steps, Coaching Questions
- [ ] `CATALOG.md` updated to match — a model missing from it is invisible to the agent
- [ ] Manifests still parse: `python3 -c "import json;json.load(open('.claude-plugin/plugin.json'))"`
- [ ] Tried locally: `claude plugin marketplace add .` then `claude plugin install mental-models@mental-models`
- [ ] `CHANGELOG.md` updated
- [ ] No duplicate of an existing model

## Notes for reviewers

<!-- Anything reviewers should focus on -->
