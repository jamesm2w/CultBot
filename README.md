# CultBot

Node.js rewrite of the original CultBot for Discord.

## Done
- Google search command
- Ping command
- Hello command
- Karma system

## TODO
- Karma blacklist
- Configuration commands

## Deploying
- Install dependencies with `npm install`

- Create a `.env` file with with the following entries
```
DISCORD_TOKEN=[Bot Token]
CLIENT_ID=[Bot Client ID]
GUILD_ID=[Primary Guild ID]
```
- Create a `emojiConfig.json` file with the following structure
```
{
    "positive": [ ],
    "negative": [ ]
}
```
- Add positive/negative emojis to the arrays as necessary (Use a string of the emoji name, which is the text of custom emojis or the actual emoji for default ones)
- Register slash commands with `npm run commands`
- Launch bot with `npm start`

## Dependencies
Install with `npm install`
- `node v16.8` (Other versions not tested) 
- `discord.js v13.1.0`
- `dotenv v10.0.0`
- `sequelize v6.6.5`
- `sqlite3 v4.2.0`
