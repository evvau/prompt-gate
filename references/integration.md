# Автоматическая интеграция Prompt Gate

Добавлять эти фрагменты в существующие настройки. Не перезаписывать посторонние инструкции и параметры пользователя.

## Поддерживаемые окружения

| Клиент | Windows 10/11 | Ubuntu 20.04+ и другой Linux |
| --- | --- | --- |
| Codex CLI | `%USERPROFILE%\\.agents\\skills\\prompt-gate` | `~/.agents/skills/prompt-gate` |
| Claude Code CLI | `%USERPROFILE%\\.claude\\skills\\prompt-gate` | `~/.claude/skills/prompt-gate` |

Сам `SKILL.md` не зависит от ОС. Различаются только пути, оболочка и команда запуска Claude hook. Для Codex CLI отдельного hook-скрипта нет.

## Codex: глобальный режим проверки

Установить skill в `$HOME/.agents/skills/prompt-gate/`. Добавить раздел в глобальный файл инструкций Codex `~/.codex/AGENTS.md`:

```markdown
## Prompt Gate

- Перед каждой новой задачей, предполагающей выполнение действий, вызывать `$prompt-gate` в режиме проверки.
- Во время проверки разрешать только чтение и минимальную сверку с официальной документацией.
- Не изменять файлы, не запускать команды проекта и не вызывать изменяющие инструменты, пока пользователь не напишет `ЗАПУСКАЙ` или `EXECUTE`.
- После подтверждения выполнять последний предложенный prompt без повторной проверки, если пользователь существенно его не изменил.
- Если ранее предложенного prompt нет, попросить пользователя прислать запрос.
```

Codex применяет это правило через постоянные инструкции. Это не нативный pre-submit hook.

## Claude Code: skill и глобальная инструкция

Установить skill в `~/.claude/skills/prompt-gate/`. Добавить раздел в `~/.claude/CLAUDE.md`:

```markdown
## Prompt Gate

Считать системное напоминание PROMPT GATE обязательным. Для новой задачи использовать `/prompt-gate` в режиме проверки и не вызывать изменяющие инструменты. После команды `ЗАПУСКАЙ` или `EXECUTE` выполнять последний предложенный prompt. Если предложения нет, запросить prompt, ничего не придумывая.
```

## Claude Code: UserPromptSubmit hook

Добавить подходящий вариант в существующий `~/.claude/settings.json`.

Windows:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "py \"$env:USERPROFILE\\.claude\\skills\\prompt-gate\\scripts\\claude_user_prompt_hook.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Ubuntu/Linux:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.claude/skills/prompt-gate/scripts/claude_user_prompt_hook.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Command hook работает детерминированно и не делает отдельный LLM-запрос. Он добавляет короткое системное напоминание перед каждым prompt. Команда подтверждения переключает его в режим выполнения, предотвращая цикл повторных проверок.

Перед настройкой проверить CLI и интерпретатор:

- Windows: `codex --version`, `claude --version`, `py -3 --version`;
- Ubuntu/Linux: `codex --version`, `claude --version`, `python3 --version`.

После установки в Codex CLI использовать `/skills` или упоминание `$prompt-gate`. В Claude Code CLI использовать `/prompt-gate` и `/hooks` для проверки hook.

## Быстрая проверка

1. Открыть новую сессию Codex или Claude Code.
2. Отправить: `Добавь CSV-экспорт в этот проект`.
3. Убедиться, что агент предложил исправленный prompt и ничего не изменил.
4. Отправить: `ЗАПУСКАЙ`.
5. Убедиться, что агент выполнил ранее предложенный prompt без повторной проверки.
