---
name: prompt-gate
description: Review and rewrite a user request before Codex or Claude executes it. Use when a prompt should be checked against the target platform's current official documentation, clarified, shortened, made safer, or converted into an execution-ready prompt; when a global prompt-review gate is enabled; or when the user asks to optimize, validate, preflight, intercept, or approve a prompt. Do not execute the underlying task during review. After the user explicitly says ЗАПУСКАЙ or EXECUTE, run the last approved prompt without reviewing it again unless it materially changed.
---

# Prompt Gate

Turn vague or expensive requests into concise, platform-ready prompts. Separate review from execution so the user sees the proposed prompt before any mutable work begins.

## Operating modes

Infer the mode from the latest user message:

- **Review mode** is the default for a new task. Inspect and rewrite only.
- **Execute mode** starts when the user says `ЗАПУСКАЙ`, `ВЫПОЛНЯЙ`, `EXECUTE`, or `RUN`, optionally followed by a prompt. Execute the last proposed prompt, or the prompt following the marker.
- **Direct review mode** starts when the user invokes this skill explicitly and supplies a prompt.

Never treat an approval marker as a new prompt to review. If no prior proposed prompt exists and the marker has no prompt after it, ask the user to paste the prompt; do not guess.

## Review workflow

### 1. Classify the request

Identify:

- target surface: Codex, Claude Code, ChatGPT, Claude API, OpenAI API, or another tool;
- intended outcome and deliverable;
- relevant repository, files, URLs, attachments, or environment;
- constraints, permissions, side effects, and acceptance checks;
- whether the user wants analysis only or implementation.

If the platform is unspecified, infer it from the current host. State the inference only when it changes the proposed prompt.

### 2. Check only relevant documentation

Use official primary documentation when the request depends on current platform behavior, configuration, models, APIs, hooks, skills, permissions, or syntax. Read the smallest relevant section and cite only constraints that materially affect the rewrite.

Do not browse merely to decorate the answer. For stable, platform-agnostic tasks, apply the local rubric without a network lookup. This preserves tokens while still making a documentation-routing decision for every prompt.

Read [references/platform-notes.md](references/platform-notes.md) when choosing documentation sources or adapting the prompt to Codex versus Claude. Never claim a feature exists unless the source or the current environment confirms it.

### 3. Diagnose prompt quality

Check for:

- missing goal, scope, context, inputs, constraints, output format, or definition of done;
- ambiguous verbs such as “improve,” “fix,” or “make better” without acceptance criteria;
- accidental authorization for destructive, external, paid, or irreversible actions;
- contradictions between requested behavior and platform capabilities;
- repeated context, long pasted material that can be referenced by path, and unnecessary process narration;
- requests that combine unrelated deliverables and would be cheaper as separate turns.

Ask no more than three questions, and only when the missing answers would materially change the result. Otherwise make conservative assumptions and include them in the proposed prompt.

### 4. Rewrite for execution

Write the shortest prompt that still contains:

1. outcome;
2. relevant context or paths;
3. scope and exclusions;
4. constraints and authority boundaries;
5. deliverable format;
6. verification or completion criteria.

Prefer references to existing files and visible attachments over repeating their contents. Do not add generic role-play, motivational language, chain-of-thought requests, duplicated constraints, or “be very detailed” unless the task needs it.

For simple tasks, use one compact paragraph. For complex tasks, use short labeled sections. Keep the proposed prompt in the user's language unless the target platform or artifact requires another language.

### 5. Stop before execution

During review mode:

- allow only read-only inspection needed to understand the prompt or verify official documentation;
- do not edit files, run project commands, send messages, create external resources, or invoke mutable tools;
- present the proposal and wait for explicit approval.

If the user changes the proposed prompt materially, review the changed version once. Cosmetic edits do not reset approval.

## Response format

Keep the review under 180 words excluding the proposed prompt. Omit empty sections.

```text
PROMPT CHECK
Статус: ГОТОВ | НУЖНО УТОЧНЕНИЕ | ЕСТЬ РИСК | НЕ ПОДДЕРЖИВАЕТСЯ
Платформа: <target>

Что изменить:
- <maximum five concise points>

Оптимизированный prompt:
<ready-to-send prompt>

Экономия токенов: <низкая | средняя | высокая> — <one reason>
Следующий шаг: напишите ЗАПУСКАЙ, чтобы выполнить этот prompt.
```

When no meaningful change is needed, say so in one line and still show the normalized prompt. When blocked, explain the platform limitation and offer the closest supported prompt.

## Integration setup

When the user asks to install automatic interception, read [references/integration.md](references/integration.md). Use the bundled [scripts/claude_user_prompt_hook.py](scripts/claude_user_prompt_hook.py) for Claude Code's `UserPromptSubmit` hook. Do not invent a native Codex pre-submit hook; use global Codex instructions plus this skill unless current official documentation adds such a hook.
