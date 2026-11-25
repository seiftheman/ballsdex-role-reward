# Commands

The package exposes one owner-only command for manual checks. Automatic checks run every
five minutes without any command input.

## `rolereward`

Manually runs the progression check for the configured server.

```text
rolereward
```

| Property | Value |
| --- | --- |
| Availability | Bot owner only |
| Location | Must be used in the server configured in the settings row |
| Alias | `hello` is kept for compatibility with older installations |

The command reloads settings from the database before running, so it always uses the
latest admin configuration. If no settings row exists, it replies that settings have not
been configured yet. If it is used in another server, it explains that it can only be used
in the configured server.

### Example output

```text
Progression role check complete.
Enabled balls: 240
Required progression: 1.00%
Target: 3/240 distinct balls
Eligible players: 18
Already rewarded: 12
Members not found: 1
Newly assigned: 4
Failures: 1
```

| Counter | Meaning |
| --- | --- |
| Enabled balls | Number of enabled balls used as the progression denominator. |
| Required progression | The configured fraction, shown as a percentage. |
| Target | Distinct balls a player needs to qualify. |
| Eligible players | Players in the database who meet the target. |
| Already rewarded | Eligible members who already had the reward role. |
| Members not found | Eligible Discord IDs no longer present in the server. |
| Newly assigned | Roles successfully granted during this check. |
| Failures | Fetch or assignment failures, including permission errors. |

!!! note "Automatic checks"
    The five-minute background loop uses the same logic but writes the result to the bot
    log instead of sending a Discord message. It also skips silently when settings are
    missing or invalid.

## Errors reported by the command

If validation fails, the command sends one of these messages instead of counters:

- `Role reward settings have not been configured yet.`
- `This command can only be used in the configured server.`
- `The configured server is unavailable to the bot.`
- `The configured reward role was not found in the server.`
- `The bot needs the 'Manage Roles' permission in the configured server.`
- `The reward role is managed by Discord or is not below the bot's highest role.`
- `There are no enabled balls to calculate progression from.`

Each message is also logged by the automatic check. See
[Troubleshooting](troubleshooting.md) for how to fix them.
