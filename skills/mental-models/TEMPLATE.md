<!--
Copy this file to write your own mental model.

  .mental-models/<name>.md          this project's models — commit them with the code
  ~/.claude/mental-models/<name>.md your personal models, available everywhere

Name the file after the idea, in lowercase with hyphens: blast-radius-first.md

The frontmatter below is Open Knowledge Format. Only `type` is required; everything else
is optional, and `sources` is the one worth the effort. A model whose claims trace to
something real is worth more than three that don't.
-->
---
type: mental-model
title: <Title Case Name>
description: <one sentence — what the model does, not what topic it is about>
tags:
- <area, e.g. incident-response>
- <situation, e.g. outage>
- <the words you would actually use when you have this problem>
status: draft
sources:
- id: <short-key>
  resource: <URL, book page, internal doc, or a link to the incident it came from>
  title: <what it is>
  author: <who>
---

<!--
Two or three paragraphs. What the idea is, where it came from, and what it lets you see
that you'd otherwise miss. Cite claims inline with [^short-key] pointing at a `sources` id.

If it came from something that happened to you, say so — that provenance is worth more
than a citation to a famous book, because nobody else has it.
-->

## When to Avoid

<!--
The section that does the real work, and the reason to write your own model at all.
Conditions where this model actively misleads you — not generic caveats.

Bad:  "Don't apply it rigidly."
Good: "Not for chronic degradation — there's no expanding radius, so it manufactures
       urgency and burns the team on something that needed a project, not a page."
-->
- **<Condition>:** <what it does wrong here, and why>
- **<Condition>:** <what it does wrong here, and why>

## Thinking Steps

<!--
4-6 actions the reader takes, in order. Actions, not descriptions of the concept.
Each step should be something you could catch yourself failing to do.
-->
1. **<Step name>:** <what to do>
2. **<Step name>:** <what to do>
3. **<Step name>:** <what to do>
4. **<Step name>:** <what to do>

## Coaching Questions

<!-- 4-6 questions someone would actually say out loud to make you apply this. -->
- "<question>"
- "<question>"
- "<question>"
- "<question>"
