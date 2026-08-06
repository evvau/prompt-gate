# Prompt Gate

Кроссплатформенная предварительная проверка и оптимизация prompts перед выполнением в **Codex CLI** или **Claude Code CLI**.

Prompt Gate сначала показывает замечания и готовый исправленный prompt, затем ждёт явную команду `ЗАПУСКАЙ` или `EXECUTE`. До подтверждения он не должен изменять файлы или запускать изменяющие инструменты.

> Используется локальный **hook**, а не webhook. Внешний сервер и API-ключ для базового режима не нужны.

## Поддерживаемые платформы

| Система | Codex CLI | Claude Code CLI |
| --- | --- | --- |
| Windows 10/11 | Skill + `AGENTS.md` | Skill + `CLAUDE.md` + `UserPromptSubmit` |
| Ubuntu 20.04+ | Skill + `AGENTS.md` | Skill + `CLAUDE.md` + `UserPromptSubmit` |

Полная пошаговая инструкция:

**[INSTALL.md — Windows, Ubuntu, Codex CLI и Claude Code CLI](INSTALL.md)**

## Что делает

- определяет целевую платформу, ОС и ожидаемый результат;
- находит недостающий контекст, ограничения и критерии готовности;
- выявляет рискованные, платные, внешние и необратимые действия;
- сверяется только с релевантной официальной документацией;
- удаляет повторы и лишние инструкции, экономя токены;
- предлагает короткий prompt, готовый к выполнению;
- ждёт явного подтверждения пользователя.

## Как работает

1. Пользователь отправляет обычный запрос.
2. Prompt Gate включает режим проверки.
3. Skill показывает недостатки и исправленный prompt.
4. Пользователь пишет `ЗАПУСКАЙ` или `EXECUTE`.
5. Codex или Claude выполняет последний одобренный prompt без повторной проверки.

Если пользователь существенно изменил предложенный запрос, Prompt Gate проверяет новую версию ещё раз.

## Пример

Исходный запрос:

```text
Сделай сайт красиво, подключи базу, оплату и сразу опубликуй.
```

Ответ Prompt Gate:

```text
PROMPT CHECK
Статус: ЕСТЬ РИСК

Что изменить:
- Указать проект и объём первой версии.
- Определить критерии готовности.
- Не разрешать оплату и публикацию без отдельного подтверждения.

Оптимизированный prompt:
Работай с указанным проектом. Сначала изучи существующий стек.
Реализуй локальный MVP без подключения платежей и публикации.
Сохрани секреты в переменных окружения, запусти проверки и
предоставь перечень изменённых файлов и результаты тестов.

Следующий шаг: напишите ЗАПУСКАЙ.
```

## Использование в CLI

Codex CLI:

```text
$prompt-gate Проверь и оптимизируй этот запрос: ...
```

Claude Code CLI:

```text
/prompt-gate Проверь и оптимизируй этот запрос: ...
```

После получения исправленного prompt:

```text
ЗАПУСКАЙ
```

## Кроссплатформенность

- `SKILL.md` не зависит от операционной системы.
- Bundled hook написан на Python 3 и использует только стандартную библиотеку.
- На Windows hook запускается через `py -3` в PowerShell.
- На Ubuntu/Linux hook запускается через `python3` в Bash.
- Codex CLI и Claude Code CLI используют официальные пользовательские каталоги skills.

## Ограничения

- Claude Code CLI поддерживает настоящий `UserPromptSubmit` hook до обработки prompt моделью.
- Codex CLI использует instruction-level gate через skill и глобальный `AGENTS.md`; это не жёсткая граница безопасности.
- Для принудительного запрета отдельных инструментов нужна отдельная политика разрешений или `PreToolUse` hook.

## Состав

```text
prompt-gate/
├── SKILL.md
├── INSTALL.md
├── README.md
├── agents/openai.yaml
├── assets/icon.svg
├── references/integration.md
├── references/platform-notes.md
└── scripts/claude_user_prompt_hook.py
```

## English summary

Prompt Gate is a cross-platform skill for Windows and Ubuntu that reviews and rewrites requests before Codex CLI or Claude Code CLI performs mutable work. It identifies missing context and risky actions, checks relevant official documentation when needed, proposes a token-efficient execution-ready prompt, and waits for `EXECUTE` or `RUN`.

- Codex CLI: install as a personal skill and enable the global `AGENTS.md` rule.
- Claude Code CLI: install as a personal skill and configure the bundled `UserPromptSubmit` hook.
- See [INSTALL.md](INSTALL.md) for Windows and Ubuntu commands.
