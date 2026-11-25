# Configuration

## Create the settings row

In the Django admin panel, open **Role reward settings** and add a single row.
Only one settings row is allowed; adding a second one is rejected by validation.

| Field | Description |
| --- | --- |
| `server` | Discord ID of the server that contains the reward role. |
| `role` | Discord ID of the role to grant to eligible players. |
| `progression` | Fraction of enabled balls required, between `0` and `1`. |

Examples of valid progression values:

| Value | Required collection |
| --- | --- |
| `0.01` | 1% of enabled balls |
| `0.1` | 10% of enabled balls |
| `0.5` | 50% of enabled balls |
| `1.0` | Every enabled ball |

Values of `0`, negative values, and values above `1` are rejected because they
would either reward everyone immediately or make the reward impossible to earn.

Changes made in the admin panel are applied immediately through Django signals.
You do not need to restart the bot after editing settings.

## Discord permissions

The bot needs the **Manage Roles** permission in the configured server. The
reward role must also be:

- below the bot's highest role in the role hierarchy,
- not managed by an integration (for example, a Twitch or Boost role),
- not the `@everyone` role.

If any of these conditions fail, the check stops and logs or reports an error
instead of attempting to assign roles.

## How progression is calculated

The package counts the number of **distinct enabled balls** each player owns and
compares it with the total number of enabled balls in the database:

```text
target = ceil(total_enabled_balls × progression)
```

A player is eligible when their distinct-ball count is at least `target`.
Deleted ball instances and disabled balls are ignored. The target is always
rounded up, so even a very small progression requires at least one ball.

The automatic check runs every 5 minutes. It only grants roles; it does not
remove them if a player later stops meeting the threshold.
