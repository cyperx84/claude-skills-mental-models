## Summary

<!-- What does this PR change and why? -->

## Type

- [ ] New model
- [ ] Edit to an existing model
- [ ] Skill instructions (`SKILL.md`)
- [ ] Docs
- [ ] Plugin manifests

## Checklist

- [ ] Frontmatter has a non-empty `type` (OKF requires it)
- [ ] `sources` entries have resolvable `resource` links, and I checked they load
- [ ] Every `[^id]` in the body matches a `sources[].id`
- [ ] All four parts present: description prose, When to Avoid, Thinking Steps, Coaching Questions
- [ ] `models/index.md` updated — a model missing from it is invisible to the agent
- [ ] Manifests still parse as JSON
- [ ] Tried locally via `claude plugin marketplace add .` (remember: a version bump alone doesn't refresh the cache)
- [ ] `CHANGELOG.md` updated

## Notes for reviewers

<!-- Anything reviewers should focus on -->
