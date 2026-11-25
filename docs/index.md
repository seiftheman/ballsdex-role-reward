# ballsdex-role-reward

A [BallsDex](https://github.com/BallsDex-DiscordBot/BallsDex-DiscordBot) package
that grants a Discord role to players who reach a configured collection
progression — for example, giving access to a channel where other dexes spawn.

## Features

- Configurable server, reward role, and progression threshold in the Django admin.
- Live settings reload when the settings row is saved or deleted.
- Automatic checks every 5 minutes, plus an owner-only manual check command.
- Permission and role-hierarchy validation before any roles are assigned.
- Detailed counters for granted, skipped, missing, and failed assignments.

## Quick start

Add the package to `config/extra.toml`:

```toml
[[ballsdex.packages]]
location = "git+https://github.com/seiftheman/ballsdex-role-reward.git@v1.3.0#main"
path = "role_reward"
enabled = true
```

Restart the bot, then create a single **Role reward settings** row in the Django
admin panel. See {doc}`installation` and {doc}`configuration` for details.

```{toctree}
:maxdepth: 2
:caption: Guide

installation
configuration
commands
troubleshooting
development
```

## Links

- [GitHub repository](https://github.com/seiftheman/ballsdex-role-reward)
- [Releases](https://github.com/seiftheman/ballsdex-role-reward/releases)
- [Support server](https://discord.gg/Sagg5CejWX)
