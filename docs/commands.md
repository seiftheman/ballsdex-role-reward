# Commands

## `rolereward`

Manually runs the progression check for the configured server.

```text
rolereward
```

- **Availability:** bot owner only.
- **Location:** must be used in the server configured in the settings row.
- **Alias:** `hello` is kept for compatibility with older installations.

The command reloads settings from the database before running, so it always
uses the latest admin configuration.

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

If settings are missing or invalid, the command explains the problem instead of
running the check.
