# Установка Prompt Gate

Эта инструкция устанавливает Prompt Gate глобально для всех проектов. Основные команды приведены для Windows PowerShell; ниже есть отдельный раздел для macOS и Linux.

## Что будет установлено

- skill `prompt-gate`;
- глобальное правило проверки для Codex;
- глобальная инструкция и локальный `UserPromptSubmit` hook для Claude Code;
- команда подтверждения `ЗАПУСКАЙ` или `EXECUTE`.

Prompt Gate использует **hook**, а не внешний webhook. Для базовой работы сервер и API-ключ не нужны.

## Вариант 1: Windows — Codex

### 1. Установить skill

Открыть PowerShell и выполнить:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.agents\skills"
git clone https://github.com/evvau/prompt-gate.git "$env:USERPROFILE\.agents\skills\prompt-gate"
```

Если команда `git` не найдена, скачать ZIP через кнопку **Code → Download ZIP**, распаковать архив, переименовать папку в `prompt-gate` и поместить её сюда:

```text
%USERPROFILE%\.agents\skills\prompt-gate
```

Внутри папки должен находиться файл:

```text
%USERPROFILE%\.agents\skills\prompt-gate\SKILL.md
```

### 2. Включить автоматическую проверку

Создать папку настроек и открыть глобальный файл инструкций:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex"
notepad "$env:USERPROFILE\.codex\AGENTS.md"
```

Добавить в конец файла, сохранив существующие инструкции:

```markdown
## Prompt Gate

- Перед каждой новой задачей, предполагающей выполнение действий, вызывай `$prompt-gate` в режиме проверки.
- Во время проверки разрешены только чтение и минимальная сверка с официальной документацией.
- Не изменяй файлы, не запускай команды проекта и не вызывай изменяющие инструменты, пока пользователь не напишет `ЗАПУСКАЙ` или `EXECUTE`.
- После подтверждения выполняй последний предложенный prompt без повторной проверки, если пользователь существенно его не изменил.
- Если ранее предложенного prompt нет, попроси пользователя прислать запрос.
```

Если в `%USERPROFILE%\.codex` уже существует непустой `AGENTS.override.md`, Codex использует его вместо глобального `AGENTS.md`. В таком случае добавить этот раздел в `AGENTS.override.md`.

### 3. Проверить Codex

Открыть новую сессию Codex и отправить:

```text
$prompt-gate Проверь запрос: добавь CSV-экспорт в текущий проект
```

Ожидаемый результат: Codex показывает замечания и исправленный prompt, но не меняет файлы. Для выполнения написать:

```text
ЗАПУСКАЙ
```

## Вариант 2: Windows — Claude Code

### 1. Установить skill

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"
git clone https://github.com/evvau/prompt-gate.git "$env:USERPROFILE\.claude\skills\prompt-gate"
```

При установке из ZIP итоговый файл должен находиться здесь:

```text
%USERPROFILE%\.claude\skills\prompt-gate\SKILL.md
```

### 2. Проверить Python

Hook запускается локальным Python-скриптом:

```powershell
py --version
```

Если команда не найдена, установить Python 3 и убедиться, что команда `py` работает.

### 3. Добавить глобальное правило Claude

Открыть файл:

```powershell
notepad "$env:USERPROFILE\.claude\CLAUDE.md"
```

Добавить в конец, не удаляя существующие инструкции:

```markdown
## Prompt Gate

Считай системное напоминание PROMPT GATE обязательным. Для новой задачи используй `/prompt-gate` в режиме проверки и не вызывай изменяющие инструменты. После команды `ЗАПУСКАЙ` или `EXECUTE` выполняй последний предложенный prompt. Если предложения нет, запроси prompt, ничего не придумывая.
```

### 4. Подключить UserPromptSubmit hook

Открыть пользовательские настройки Claude Code:

```powershell
notepad "$env:USERPROFILE\.claude\settings.json"
```

Добавить объект `UserPromptSubmit` внутрь существующего объекта `hooks`. Не заменять весь файл, если в нём уже есть другие настройки или hooks.

Для нового пустого файла использовать:

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

### 5. Проверить Claude Code

В Claude Code выполнить:

```text
/hooks
```

В разделе `UserPromptSubmit` должен отображаться command hook из пользовательских настроек. Затем отправить:

```text
/prompt-gate Проверь запрос: добавь CSV-экспорт в текущий проект
```

Claude должен предложить исправленный prompt и остановиться до команды:

```text
ЗАПУСКАЙ
```

## macOS и Linux — Codex

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/evvau/prompt-gate.git ~/.agents/skills/prompt-gate
mkdir -p ~/.codex
```

Добавить раздел Prompt Gate из инструкции для Windows в `~/.codex/AGENTS.md`, затем проверить skill командой:

```text
$prompt-gate Проверь запрос: добавь CSV-экспорт в текущий проект
```

## macOS и Linux — Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/evvau/prompt-gate.git ~/.claude/skills/prompt-gate
python3 --version
```

Добавить правило Prompt Gate в `~/.claude/CLAUDE.md`. Затем добавить в существующий `~/.claude/settings.json`:

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

## Установка только для одного проекта

Если skill не должен действовать глобально, разместить его внутри конкретного проекта:

| Платформа | Папка проекта |
| --- | --- |
| Codex | `.agents/skills/prompt-gate/` |
| Claude Code | `.claude/skills/prompt-gate/` |

Глобальные файлы `~/.codex/AGENTS.md` и `~/.claude/CLAUDE.md` в этом варианте не изменять. Проектные правила можно добавить в `AGENTS.md` или `CLAUDE.md` самого проекта.

## Обновление

Codex на Windows:

```powershell
git -C "$env:USERPROFILE\.agents\skills\prompt-gate" pull
```

Claude Code на Windows:

```powershell
git -C "$env:USERPROFILE\.claude\skills\prompt-gate" pull
```

macOS/Linux: выполнить `git pull` внутри соответствующей папки `prompt-gate`.

## Устранение проблем

- Skill не найден: проверить, что `SKILL.md` лежит непосредственно внутри папки `prompt-gate`, без дополнительного уровня `prompt-gate-main`.
- Codex сразу выполняет задачу: проверить глобальный `AGENTS.md` и наличие `AGENTS.override.md`.
- Claude не запускает hook: выполнить `/hooks`, проверить путь к скрипту и команду `py --version` или `python3 --version`.
- Подтверждение снова проверяется: использовать отдельное сообщение `ЗАПУСКАЙ` или `EXECUTE`.
- Не перезаписывать существующий `settings.json`: объединять новые hooks с имеющимися настройками.

## Официальная документация

- [Codex: Build skills](https://developers.openai.com/codex/build-skills)
- [Codex: AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md)
- [Claude Code: Skills](https://code.claude.com/docs/en/skills)
- [Claude Code: Hooks](https://code.claude.com/docs/en/hooks)
