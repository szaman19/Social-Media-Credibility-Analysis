#! usr/bin/python3

# group06 IP - 128.226.28.226

import pymongo
import praw
import json
from datetime import datetime

# personal use script - CEOYoodNamWo9w
# secret key - V3wTJlF0EanqoQdkPv81xb-mw18

def get_comments(submission):
    submission.comments.replace_more(limit=None) #returns depth-first search of comment tree
    comments = {}
    for comment in submission.comments.list():
        comment_dict = {}
        comment_dict["body"] = comment.body
        comment_dict["score"] = comment.score
        comment_dict["time_submitted"] = comment.created_utc
        comments[comment.id] = comment_dict
    return comments

def get_posts(subreddit, submissions):
    for submission in reddit.subreddit(subreddit).new(limit=500):
        submission_info = {}
        submission_info["subreddit"] = sub_name
        submission_info["title"]= submission.title
        submission_info["score"] = submission.score
        submission_info["url"] = submission.url
        submission_info["comms_num"] = submission.num_comments
        submission_info["created"] = submission.created
        submission_info["body"] = submission.selftext

        submission_info["comments"] = get_comments(submission)
        submissions[submission.id] = submission_info

def main():
    reddit = praw.Reddit(client_id='CEOYoodNamWo9w', \
                         client_secret='V3wTJlF0EanqoQdkPv81xb-mw18', \
                         user_agent='CS480N Social Media Scraper')

    submissions = {}
    subs = ('politics', 'worldpolitics', 'The_Donald', 'news', 'worldnews', 'Worldevents')
    for sub_name in subs:
        get_posts(sub_name, submissions)

    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(f'collected at {time}.json', 'w') as json_file:
        json.dump(submissions, json_file)

    print(f"file 'reddit_data_{time}.json' created")

if __name__ == '__main__':
  main()

