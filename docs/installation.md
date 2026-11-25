# Installation

## Requirements

- A working BallsDex Discord bot installation with the Django admin panel enabled.
- The bot must be a member of the Discord server that contains the reward role.

## Add the package

Add the following block to your `config/extra.toml`:

```toml
[[ballsdex.packages]]
location = "git+https://github.com/seiftheman/ballsdex-role-reward.git@v1.3.0#main"
path = "role_reward"
enabled = true
```

Replace `v1.3.0` with the version you want to install. Pinning a version is
recommended so that updating BallsDex or another package does not silently
upgrade this one.

Restart the bot so the package is loaded and its database migration is applied.
The cog starts even if no settings exist yet; it simply skips checks until you
configure a settings row.

## Verify the installation

1. Open the Django admin panel for your bot.
2. Confirm a **Role reward settings** section appears under *Role reward*.
3. Continue with {doc}`configuration`.

If the section does not appear, check the bot log for package loading errors and
make sure `path = "role_reward"` matches the package directory name.
