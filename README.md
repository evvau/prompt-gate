# Prompt Gate

Предварительная проверка и оптимизация prompts перед выполнением в **Codex** или **Claude Code**.

Prompt Gate отделяет подготовку запроса от его выполнения: сначала показывает замечания и готовый исправленный prompt, затем ждёт явную команду `ЗАПУСКАЙ` или `EXECUTE`.

> Технически используется **hook**, а не webhook: внешний сервер для базового режима не нужен.

## Русская версия

### Что делает

- определяет целевую платформу и ожидаемый результат;
- находит недостающий контекст, ограничения и критерии готовности;
- выявляет рискованные, платные, внешние и необратимые действия;
- решает, нужна ли сверка с актуальной официальной документацией;
- удаляет повторы и лишние инструкции, экономя токены;
- предлагает короткий готовый prompt;
- не начинает изменяющую работу до явного подтверждения пользователя.

Для стабильных задач, не зависящих от платформы, skill применяет локальные правила без ненужного сетевого поиска. Для актуальных настроек, API, hooks, skills, моделей и разрешений используются официальные источники соответствующей платформы.

### Как это работает

1. Пользователь отправляет обычный запрос.
2. Prompt Gate включает режим проверки.
3. Skill показывает недостатки и исправленный prompt.
4. Пользователь пишет `ЗАПУСКАЙ` или `EXECUTE`.
5. Codex или Claude выполняет последний одобренный prompt без повторной проверки.

Если пользователь существенно изменил предложенный запрос, Prompt Gate проверяет новую версию ещё раз.

### Пример

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

### Использование

Codex:

```text
$prompt-gate Проверь и оптимизируй этот запрос: ...
```

Claude Code:

```text
/prompt-gate Проверь и оптимизируй этот запрос: ...
```

После получения исправленного prompt:

```text
ЗАПУСКАЙ
```

### Установка

#### Codex

Скопируйте репозиторий в персональную папку skills:

- Windows: `%USERPROFILE%\.agents\skills\prompt-gate`
- macOS/Linux: `~/.agents/skills/prompt-gate`

Чтобы проверка применялась автоматически к новым задачам, добавьте глобальные правила из [references/integration.md](references/integration.md) в `~/.codex/AGENTS.md`.

#### Claude Code

Скопируйте репозиторий в:

- Windows: `%USERPROFILE%\.claude\skills\prompt-gate`
- macOS/Linux: `~/.claude/skills/prompt-gate`

Затем подключите локальный `UserPromptSubmit` hook по инструкции в [references/integration.md](references/integration.md). Скрипт [scripts/claude_user_prompt_hook.py](scripts/claude_user_prompt_hook.py) не выполняет отдельный LLM-запрос.

### Ограничения

- В Claude Code используется настоящий `UserPromptSubmit` hook до обработки prompt моделью.
- В Codex применяется instruction-level gate через skill и глобальный `AGENTS.md`; это не системная граница безопасности.
- Для жёсткой блокировки инструментов требуется отдельная политика `PreToolUse` или разрешений.

### Состав

```text
prompt-gate/
├── SKILL.md
├── agents/openai.yaml
├── assets/icon.svg
├── references/integration.md
├── references/platform-notes.md
└── scripts/claude_user_prompt_hook.py
```

## English summary

Prompt Gate reviews and rewrites requests before Codex or Claude Code performs mutable work. It identifies missing context and risky actions, checks relevant official documentation when necessary, proposes a token-efficient execution-ready prompt, and waits for `EXECUTE` or `RUN`.

- Codex: install as a personal skill and enable the global `AGENTS.md` rule.
- Claude Code: install as a personal skill and configure the bundled `UserPromptSubmit` hook.
- Full operating instructions are in [SKILL.md](SKILL.md).
