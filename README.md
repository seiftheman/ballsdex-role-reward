# ballsdex-role-reward

Ever got a support server for your dex and has a channel that other dexes spawn in? Well, this is for you. This package gives a role (that you specify), that has access to that channel, to a user that reached a required progression in your dex. Cool, right?

## Installation

Add the following into your `config/extra.toml` file.

```toml
[[ballsdex.packages]]
location = "git+https://github.com/seiftheman/ballsdex-role-reward.git@v1.3.0#main"
path = "role_reward"
enabled = true
```

## Configuration

After restarting the bot, open the Django admin panel and add a single
**Role reward settings** row (under *Role reward*):

| Field | Description |
| --- | --- |
| `server` | The ID of the Discord server that contains the reward role. |
| `role` | The ID of the role to give to eligible players. |
| `progression` | A fraction between 0 and 1, e.g. `0.01` for 1% of the collection. |

Only one settings row is allowed. It is reloaded automatically when saved or
deleted in the admin panel, so there is no need to restart the bot.

Progression is measured as the number of **distinct enabled balls** a player
owns divided by the total number of enabled balls. The required count is
rounded up, so even a very small progression requires at least one ball. The
check runs every 5 minutes and grants the role to everyone who qualifies.

The bot needs the **Manage Roles** permission in the configured server, and the
reward role must be below the bot's highest role and not managed by Discord.

## Manual check

The bot owner can trigger a check on demand in the configured server with:

```
rolereward
```

The old `hello` command remains available as an alias. The output summarises
how many players were eligible, how many roles were granted, and any failures.

## Documentation

Full documentation is hosted on [Read the Docs](https://ballsdex-role-reward.readthedocs.io/).

## Development

Install the development dependencies (`pytest`, `pytest-asyncio`, `Django` and
`discord.py`) and run:

```bash
pytest
```

## Contact

- You can contact me via the **official Discord server**.  
[![Discord](https://img.shields.io/discord/1433459095129559170?label=Support%20Server&logo=discord&color=7289DA&logoColor=white)](https://discord.gg/Sagg5CejWX)
