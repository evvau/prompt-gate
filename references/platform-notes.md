# Platform notes

Use this reference only when the target platform affects the rewrite.

## Source routing

Prefer these official sources and load only the relevant page or section:

| Target | Primary sources | Typical checks |
| --- | --- | --- |
| Codex / ChatGPT Work | `learn.chatgpt.com`, `developers.openai.com`, `platform.openai.com` | Skills, `AGENTS.md`, modes, permissions, API syntax, supported tools |
| Claude Code / Claude API | `code.claude.com`, `docs.anthropic.com`, `support.claude.com` | Skills, hooks, `CLAUDE.md`, permissions, API syntax, supported tools |
| Third-party framework | Official docs and official source repository | Current version, command syntax, configuration, deprecations |

Avoid blogs and search snippets when an official page exists. If current documentation cannot be reached, disclose that the rewrite uses known behavior and mark version-sensitive claims as assumptions.

## Codex adaptation

Codex works best when the prompt names the outcome, relevant paths, constraints, expected verification, and whether the agent may implement or should only inspect. Put durable project rules in `AGENTS.md`; put repeatable workflows in skills.

Codex has no documented equivalent of Claude Code's `UserPromptSubmit` hook as of this skill version. For automatic review, global `AGENTS.md` must require this skill before mutable work. Describe this as an instruction-level gate, not a hard runtime interceptor.

## Claude Code adaptation

Claude Code supports skills, global `CLAUDE.md`, and hooks. `UserPromptSubmit` runs before Claude processes a prompt and can add context or block the prompt. The bundled hook adds a short system reminder without a second model call; Claude then uses this skill to perform the review.

The hook plus `CLAUDE.md` is a behavioral gate. A hard security boundary against tool use requires a separately designed `PreToolUse` policy and must not be implied by this skill.

## Token-efficiency rules

- Reuse repository paths and attachments instead of pasting their contents.
- Do not repeat platform documentation in the proposed prompt; encode only the resulting constraint.
- Prefer one deliverable per prompt when tasks are independent.
- Ask only blocking questions.
- Keep validation commands specific to the changed scope.
- Do not request hidden chain-of-thought; ask for conclusions, evidence, diffs, or test results.
