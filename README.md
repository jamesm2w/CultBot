# CultBot

Node.js rewrite of the original CultBot for Discord.

## Done
- Google search command
- Ping command
- Hello command

## TODO
- karma system

## Deploying
- Install dependencies with `npm install`

- Create a `.env` file with with the following entries
```
DISCORD_TOKEN=[Bot Token]
CLIENT_ID=[Bot Client ID]
GUILD_ID=[Primary Guild ID]
```

- Register slash commands with `npm run commands`
- Launch bot with `npm start`

## Dependencies
Install with `npm install`
- `node v16.8` (Other versions not tested) 
- `discord.js v13.1.0`
- `dotenv v10.0.0`
