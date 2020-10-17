import time
import traceback

import praw
import prawcore
import schedule

import CONFIG

# Only works in the subreddit mentioned in CONFIG
import CONSTANTS

subreddit = CONFIG.reddit.subreddit(CONFIG.subreddit_name)

# Gets 100 historical submission
submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)


# Replies comment with body
def reply(to_submission, body):
    response = body + "\n\n ^(This action was performed by a bot, please contact the mods for any questions.)"
    new_comment = to_submission.reply(response)
    try:
        new_comment.mod.distinguish(how="yes")
    except prawcore.exceptions.Forbidden:
        print('Couldn\'t mark submission as distinguished!')


# Follows up old submissions and mark the abandoned submissions
def follow_up_old_submissions():
    saved_list = CONFIG.reddit.redditor(CONFIG.username).saved(limit=None)
    for saved in saved_list:
        # Make sure it doesn't try to process comments
        if type(saved) != praw.models.Submission:
            continue
        # If the flair isn't marked solved
        if saved.link_flair_text != 'Solved':
            # Checking submission age
            now = time.time()
            submission_age = now - saved.created_utc
            # If the age is over abandoned_days_limit, sets flair to abandoned
            if submission_age >= (CONSTANTS.ABANDONED_DAYS_LIMIT * 86400):
                saved.flair.select(CONSTANTS.ABANDONED_ID)
                saved.unsave()
            # If age just crossed the follow up limits. Sends a follow up comment
            elif submission_age >= (CONSTANTS.FOLLOW_UP_DAYS_LIMIT * 86400):
                reply(saved, CONSTANTS.FOLLOW_UP_COMMENT)
        # Unsave the submissions that are already Solved
        elif saved.link_flair_text != 'Solved':
            saved.unsave()


schedule.every(1).days.do(follow_up_old_submissions())

while True:
    # Try catch to make sure bot doesn't go down during Server errors or if internet goes down
    try:
        # Initialize scheduler
        schedule.run_pending()
        # Gets posts and if it receives None, it switches to mentions
        for submission in submission_stream:
            if submission is None:
                break
                # Saving all submissions that get posted
                submission.save()
    except Exception:
        # Print the error
        tb = traceback.format_exc()
        print(tb)
        # Try again in 30 seconds
        time.sleep(30)
        # Recreates streams generator
        comment_stream = subreddit.stream.comments(pause_after=-1, skip_existing=True)
