# Troubleshooting

## `Role reward settings have not been configured.`

No settings row exists, or its values failed validation. Open the Django admin
panel and create or fix the single **Role reward settings** row. Progression
must be greater than `0` and at most `1`, and both IDs must be numeric Discord
snowflakes.

## `The configured server is unavailable to the bot.`

The bot is not in the server ID stored in the settings row, or Discord has not
finished filling its guild cache yet. Invite the bot to the correct server and
wait for it to become ready.

## `The configured reward role was not found in the server.`

The role ID does not exist in the configured server. Copy the role ID again
(Discord developer mode → right-click role → **Copy ID**) and update the
settings row.

## `The bot needs the 'Manage Roles' permission...`

Grant the bot the **Manage Roles** permission in the configured server, either
through a role or a channel-independent server permission.

## `The reward role is managed by Discord or is not below the bot's highest role.`

Discord only allows a bot to assign roles below its own highest role. Move the
bot's role above the reward role in **Server Settings → Roles**, or choose a
different reward role. Integration-managed and `@everyone` roles cannot be
assigned.

## `There are no enabled balls to calculate progression from.`

All balls are currently disabled in BallsDex. Enable at least one ball before
running the reward check.

## Members are reported as not found

Those player records still have eligible collections, but the Discord members
are no longer in the server (or cannot be fetched). The package skips them and
continues with the remaining members.

## Roles are assigned but failures are reported

Usually this means the bot lost **Manage Roles** permission mid-run, the reward
role was deleted, or Discord returned an HTTP error. The bot log contains the
exception with the affected member ID.
