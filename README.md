
# ApplianceRepairBot
This is a reddit bot for [ApplianceRepairBot](https://www.reddit.com/r/appliancerepair/). The bot follow ups users who haven't marked their submissions solved after certain amount of days. If the user doesn't mark the post Solved within a certain amount of days, it gets flaired as abandoned. 

### How to use the bot
In order to run the bot, you need to create CONFIG.py using the template given below
```
import praw

# Login information
username = ''
password = ''

# API information
client_id = ''
client_secret = ''
user_agent = ''

# Put the name of your subreddit here
subreddit_name = ""

# Login Api
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

```
After adding the config file, make sure that the flair IDs in CONSTANTS.py are correct and updated.

*For more questions, contact the mods of r/appliancerepair or me(u/is_fake_account)*