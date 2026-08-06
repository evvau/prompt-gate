# Установка Prompt Gate

Prompt Gate поддерживает:

| Операционная система | Codex CLI | Claude Code CLI |
| --- | --- | --- |
| Windows 10/11 | Да | Да |
| Ubuntu 20.04+ | Да | Да |

Skill работает локально. Внешний webhook, сервер и API-ключ не требуются. Для Claude Code используется локальный `UserPromptSubmit` hook; для Codex CLI — skill и глобальная инструкция `AGENTS.md`, поскольку у Codex нет документированного аналога этого hook.

## Что выбрать

- Пользуетесь Codex CLI — установите раздел для Codex.
- Пользуетесь Claude Code CLI — установите раздел для Claude.
- Пользуетесь обоими — установите skill в обе папки.
- Нужен skill только в одном репозитории — используйте раздел «Установка для одного проекта».

## Windows — Codex CLI

### 1. Проверить зависимости

Откройте PowerShell:

```powershell
git --version
codex --version
```

### 2. Установить skill глобально

```powershell
$SkillDir = Join-Path $env:USERPROFILE ".agents\skills\prompt-gate"
New-Item -ItemType Directory -Force (Split-Path $SkillDir)
git clone https://github.com/evvau/prompt-gate.git $SkillDir
Test-Path (Join-Path $SkillDir "SKILL.md")
```

Последняя команда должна вывести `True`.

Если папка уже существует, обновите её:

```powershell
git -C "$env:USERPROFILE\.agents\skills\prompt-gate" pull
```

### 3. Включить проверку всех новых задач

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex"
notepad "$env:USERPROFILE\.codex\AGENTS.md"
```

Добавьте в конец файла, не удаляя существующие правила:

```markdown
## Prompt Gate

- Перед каждой новой задачей, предполагающей выполнение действий, вызывай `$prompt-gate` в режиме проверки.
- Во время проверки разрешены только чтение и минимальная сверка с официальной документацией.
- Не изменяй файлы, не запускай команды проекта и не вызывай изменяющие инструменты, пока пользователь не напишет `ЗАПУСКАЙ` или `EXECUTE`.
- После подтверждения выполняй последний предложенный prompt без повторной проверки, если пользователь существенно его не изменил.
- Если ранее предложенного prompt нет, попроси пользователя прислать запрос.
```

Если существует непустой `%USERPROFILE%\.codex\AGENTS.override.md`, Codex использует его вместо глобального `AGENTS.md`. Тогда добавьте раздел туда.

### 4. Проверить в Codex CLI

Запустите:

```powershell
codex
```

В интерактивной сессии откройте `/skills`, убедитесь, что виден `prompt-gate`, затем отправьте:

```text
$prompt-gate Проверь запрос: добавь CSV-экспорт в текущий проект
```

Codex должен предложить исправленный prompt и остановиться до команды `ЗАПУСКАЙ`.

## Windows — Claude Code CLI

### 1. Проверить зависимости

```powershell
git --version
claude --version
py -3 --version
```

Python 3 нужен только локальному hook и не требует дополнительных пакетов.

### 2. Установить skill глобально

```powershell
$SkillDir = Join-Path $env:USERPROFILE ".claude\skills\prompt-gate"
New-Item -ItemType Directory -Force (Split-Path $SkillDir)
git clone https://github.com/evvau/prompt-gate.git $SkillDir
Test-Path (Join-Path $SkillDir "SKILL.md")
```

### 3. Добавить глобальную инструкцию

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude"
notepad "$env:USERPROFILE\.claude\CLAUDE.md"
```

Добавьте:

```markdown
## Prompt Gate

Считай системное напоминание PROMPT GATE обязательным. Для новой задачи используй `/prompt-gate` в режиме проверки и не вызывай изменяющие инструменты. После команды `ЗАПУСКАЙ` или `EXECUTE` выполняй последний предложенный prompt. Если предложения нет, запроси prompt, ничего не придумывая.
```

### 4. Подключить UserPromptSubmit hook

Откройте пользовательские настройки:

```powershell
notepad "$env:USERPROFILE\.claude\settings.json"
```

Если файл пустой, используйте:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "py -3 \"$env:USERPROFILE\\.claude\\skills\\prompt-gate\\scripts\\claude_user_prompt_hook.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Если `settings.json` уже содержит настройки, добавьте `UserPromptSubmit` внутрь существующего объекта `hooks`; не заменяйте весь файл.

### 5. Проверить в Claude Code CLI

```powershell
claude doctor
claude
```

В Claude Code выполните `/hooks`, затем:

```text
/prompt-gate Проверь запрос: добавь CSV-экспорт в текущий проект
```

## Ubuntu — Codex CLI

### 1. Проверить зависимости

```bash
sudo apt update
sudo apt install -y git
git --version
codex --version
```

### 2. Установить skill глобально

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/evvau/prompt-gate.git "$HOME/.agents/skills/prompt-gate"
test -f "$HOME/.agents/skills/prompt-gate/SKILL.md" && echo "Prompt Gate установлен"
```

Если папка уже существует:

```bash
git -C "$HOME/.agents/skills/prompt-gate" pull
```

### 3. Включить проверку всех новых задач

```bash
mkdir -p "$HOME/.codex"
nano "$HOME/.codex/AGENTS.md"
```

Добавьте тот же раздел `## Prompt Gate`, который приведён выше для Windows Codex. Если существует непустой `~/.codex/AGENTS.override.md`, добавьте правила туда.

### 4. Проверить в Codex CLI

```bash
codex
```

В сессии откройте `/skills`, затем отправьте:

```text
$prompt-gate Проверь запрос: добавь CSV-экспорт в текущий проект
```

## Ubuntu — Claude Code CLI

### 1. Проверить зависимости

```bash
sudo apt update
sudo apt install -y git python3
git --version
python3 --version
claude --version
```

### 2. Установить skill глобально

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/evvau/prompt-gate.git "$HOME/.claude/skills/prompt-gate"
test -f "$HOME/.claude/skills/prompt-gate/SKILL.md" && echo "Prompt Gate установлен"
```

### 3. Добавить глобальную инструкцию

```bash
nano "$HOME/.claude/CLAUDE.md"
```

Добавьте раздел `## Prompt Gate`, приведённый выше для Windows Claude Code.

### 4. Подключить UserPromptSubmit hook

```bash
nano "$HOME/.claude/settings.json"
```

Если файл пустой, используйте:

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

При существующем `settings.json` объедините новый hook с текущими настройками.

### 5. Проверить в Claude Code CLI

```bash
claude doctor
claude
```

В интерактивной сессии выполните `/hooks`, затем:

```text
/prompt-gate Проверь запрос: добавь CSV-экспорт в текущий проект
```

## Установка для одного проекта

Запустите команду из корня проекта.

### Windows PowerShell

Codex CLI:

```powershell
git clone https://github.com/evvau/prompt-gate.git ".agents\skills\prompt-gate"
```

Claude Code CLI:

```powershell
git clone https://github.com/evvau/prompt-gate.git ".claude\skills\prompt-gate"
```

### Ubuntu Bash

Codex CLI:

```bash
git clone https://github.com/evvau/prompt-gate.git ".agents/skills/prompt-gate"
```

Claude Code CLI:

```bash
git clone https://github.com/evvau/prompt-gate.git ".claude/skills/prompt-gate"
```

В проектном режиме добавьте правила в `AGENTS.md` или `CLAUDE.md` проекта. Для Claude hook можно добавить в `.claude/settings.json` и изменить путь скрипта на проектный.

## Установка из ZIP

Если Git недоступен:

1. Откройте страницу репозитория.
2. Нажмите **Code → Download ZIP**.
3. Распакуйте архив.
4. Переименуйте папку в `prompt-gate`.
5. Переместите её в папку выбранного CLI из таблицы в начале инструкции.

Файл `SKILL.md` должен лежать непосредственно внутри `prompt-gate`, без дополнительного уровня `prompt-gate-main`.

## Обновление

Windows PowerShell:

```powershell
git -C "$env:USERPROFILE\.agents\skills\prompt-gate" pull
git -C "$env:USERPROFILE\.claude\skills\prompt-gate" pull
```

Ubuntu:

```bash
git -C "$HOME/.agents/skills/prompt-gate" pull
git -C "$HOME/.claude/skills/prompt-gate" pull
```

Выполняйте только команду для установленного клиента.

## Устранение проблем

- Skill не виден в Codex CLI: проверьте путь к `SKILL.md` и откройте новую сессию; затем вызовите `/skills`.
- Codex сразу выполняет задачу: проверьте `AGENTS.md` и наличие `AGENTS.override.md`.
- Skill не виден в Claude Code CLI: проверьте путь и вызовите `/prompt-gate`; если верхняя папка skills создана во время активной сессии, откройте новую сессию.
- Hook Claude не запускается: вызовите `/hooks`, `claude doctor` и проверьте `py -3 --version` либо `python3 --version`.
- Claude сообщает об ошибке JSON: проверьте запятые и кавычки в `settings.json`; stdout hook должен содержать только JSON.
- Команда `ЗАПУСКАЙ` снова проверяется: отправляйте её отдельным сообщением.

## Официальная документация

- [Codex: skills и пути установки](https://developers.openai.com/codex/build-skills)
- [Codex: глобальные инструкции AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md)
- [Codex CLI](https://developers.openai.com/codex/cli)
- [Claude Code: skills](https://code.claude.com/docs/en/skills)
- [Claude Code: hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code: установка и Ubuntu](https://code.claude.com/docs/en/setup)
