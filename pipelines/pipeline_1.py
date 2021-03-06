#!/usr/bin/env python

import os
import json
import re
import requests

from twitter import Api

# URL encoded hashtag character is %23
SCREEN_NAME = "albertheijn"

CONSUMER_KEY = os.getenv("CONSUMER_KEY", None)
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET", None)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET", None)

api = Api(CONSUMER_KEY,
          CONSUMER_SECRET,
          ACCESS_TOKEN,
          ACCESS_TOKEN_SECRET)


def main():
    results = api.GetUserTimeline(screen_name=SCREEN_NAME, count=100)
    tweets = []
    i = 1
    for s in results:
        print(str(i))
        i = i+1
        if s.in_reply_to_status_id is not None:
            try:
                replied_to = api.GetStatus(s.in_reply_to_status_id)
                is_long_conversation = re.search('[0-9]/[0-9]', s.text) or re.search('[0-9]/[0-9]', replied_to.text)
                if replied_to.in_reply_to_status_id is None and not is_long_conversation:
                    tweet = {"data": {
                                "question": replied_to.text,
                                "answer": s.text
                    }}
                    tweets.append(tweet)
            except:
                print("Error at " + str(i))

    r = requests.post('http://localhost:5000/requester/tasks', data=json.dumps({
        'userId': 2,
        'description': 'Assess Twitter webcare',
        'content': tweets,
        'questionRows': [
            {'question': 'Does the original tweet contain a complaint/issue, raise a question or something else?',
             'answerSpecification': {"type": "option",
                                     "options": ["Complaint/issue", "Question", "Other"]}},
            {'question': 'Do you think this webcare tweet has helped the user with their issue?',
             'answerSpecification': {"type": "option",
                                     "options": ["Yes", "No"]}},
            {'question': 'Do you have any further comments about this webcare tweet?',
             'answerSpecification': {'type': 'plaintext'}}
        ]
    }))

    print(str(r.status_code))


if __name__ == '__main__':
    main()
