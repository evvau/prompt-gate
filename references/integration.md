# Automatic prompt-gate integration

Merge these snippets into existing configuration. Never overwrite unrelated user settings or instructions.

## Codex: global review-first behavior

Install the skill in the personal skills directory at `$HOME/.agents/skills/prompt-gate/`. Add this section to the global Codex instruction file, normally `~/.codex/AGENTS.md`:

```markdown
## Prompt Gate

- For every new execution-oriented request, invoke `$prompt-gate` in review mode before mutable work.
- Read-only inspection and the minimum official-documentation lookup are allowed during review.
- Do not edit files, run project commands, or call mutable tools until the user says `ЗАПУСКАЙ` or `EXECUTE`.
- On approval, execute the last proposed prompt without reviewing it again unless the user materially changed it.
- If there is no prior proposed prompt, ask the user to provide one.
```

Codex applies this through persistent instructions; it is not a native pre-submit hook.

## Claude Code: skill and global instruction

Install the skill at `~/.claude/skills/prompt-gate/`. Add this section to `~/.claude/CLAUDE.md`:

```markdown
## Prompt Gate

Treat the PROMPT GATE system reminder as mandatory. For a new task, use `/prompt-gate` in review mode and do not call mutable tools. After the user says `ЗАПУСКАЙ` or `EXECUTE`, execute the last proposed prompt. If no proposal exists, ask for the prompt instead of guessing.
```

## Claude Code: UserPromptSubmit hook

Merge one command variant into `~/.claude/settings.json`.

Windows:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "py \"%USERPROFILE%\\.claude\\skills\\prompt-gate\\scripts\\claude_user_prompt_hook.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

macOS or Linux:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/prompt-gate/scripts/claude_user_prompt_hook.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

The command hook is deterministic and does not make an extra LLM request. It injects a short reminder before every prompt. Approval markers switch the reminder to execute mode, preventing an approval loop.

## Quick verification

1. Start a new Codex or Claude Code session so global instructions reload.
2. Submit: `Добавь CSV-экспорт в этот проект`.
3. Confirm that the agent proposes a refined prompt and makes no edits.
4. Submit: `ЗАПУСКАЙ`.
5. Confirm that the agent executes the previously proposed prompt instead of reviewing it again.
