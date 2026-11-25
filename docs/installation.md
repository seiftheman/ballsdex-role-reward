# Installation

`ballsdex-role-reward` is a BallsDex extension package. It runs inside your existing bot,
uses its database, and grants a Discord role when a player reaches a configured collection
progression.

!!! note "What you need"
    - BallsDex **3.0 or newer**.
    - The Django admin panel enabled.
    - The bot invited to the Discord server that contains the reward role.

## Add the package

Add the following block to your BallsDex `config/extra.toml`:

```toml
[[ballsdex.packages]]
location = "git+https://github.com/seiftheman/ballsdex-role-reward.git@v1.3.0#main"
path = "role_reward"
enabled = true
```

The `location` pins the release, `path` points at the package directory inside the
repository, and `enabled` loads it on startup. Pinning a version is recommended so that
upgrading BallsDex or another package does not silently upgrade this one.

## Restart the bot

Restart BallsDex once so Django discovers the package and applies its migrations. The cog
starts even if no settings exist yet; it simply skips checks until you configure a settings
row.

If your deployment applies migrations separately, run them before starting the bot:

```bash
python manage.py migrate
```

## Configure the reward

1. Open the Django admin panel for your bot.
2. Under **Role reward**, open **Settings**.
3. Add a single row with the Discord server ID, reward role ID, and progression fraction.
4. Save the row. The running cog picks up the change immediately.

Only one settings row is allowed. See [Configuration](configuration.md) for the full
field reference and permission requirements.

## Verify the install

1. Check that `role_reward` appears in the bot's loaded packages.
2. Confirm **Role reward settings** appears in the Django admin panel.
3. Run `rolereward` in the configured server as the bot owner.
4. Read the counters in the response to confirm eligibility and grants.

!!! tip "Nothing happens yet?"
    The package does nothing until a settings row exists. Create the row, then wait for the
    next five-minute check or run the owner command manually.

## Updating

Change the pinned version in `config/extra.toml`, then restart the bot:

```toml
[[ballsdex.packages]]
location = "git+https://github.com/seiftheman/ballsdex-role-reward.git@v1.3.0#main"
path = "role_reward"
enabled = true
```

Run the migrations if your deployment does not apply them automatically. Review the
[changelog](changelog.md) before changing an existing installation.

## Troubleshooting

If the commands are missing, make sure the package is enabled and restart the bot. If
role assignment fails, check the bot's **Manage Roles** permission and the reward role's
position in the role hierarchy. See [Troubleshooting](troubleshooting.md) for the full
list of reported errors.
