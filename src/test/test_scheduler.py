import re
import unittest
import datetime

import sys
sys.path.append("..")
from src.scheduler.scheduler import Scheduler

class ResponseMock:
    status_code = 200

    def json(self):
        request_body = {
            "subreddits":["ubuntu"],
            "dataset_name":"ubuntu_data",
            "date_from":"01/24/2022",
            "date_to":"01/28/2022",
            "post_selection": "top",
            "new_limit":"0",
            "min_length_posts":"20",
            "min_length_comments":"10",
            "comment_depth" : "1",
            "blacklist_comments":[],
            "blacklist_posts":[],
            "replace_urls" : "false",
            "replace_emojis" : "false"
        }
        data = [{"subreddit_names":"chrome","date":"2022-06-02T08:29:13.049Z","occurrence":0,"number_posts":10,"dataset_name":"tmp2","request":request_body},
                {"subreddit_names":"chrome","date":"2022-06-02T08:58:00.708Z","occurrence":7,"number_posts":10,"dataset_name":"test_ui","request":request_body}]
        return data

class RequestHandlerMock:
    def get(self, http):
        return ResponseMock()

    def post(self, http, json):
        return ResponseMock()

class loggerMock:
    def info(self,text):
        pass


class TestClassifier(unittest.TestCase):
    
    def setUp(self) -> None:
        self.today = datetime.date.today()
        pass

    def test_scheduler(self):
        scheduler = Scheduler(loggerMock(), RequestHandlerMock())
        
        scheduler.get_datasets()
        self.assertEqual(len(scheduler.overview), 1)

        scheduler.update_request_bodies()

        request = scheduler.overview[0]["request"]
        
        print(request["date_to"])
        print(request["date_from"])

        self.assertEqual(request["date_to"], datetime.date.strftime(self.today, "%m/%d/%Y"))
        expected_date = self.today + datetime.timedelta(days=-7)
        self.assertEqual(request["date_from"], datetime.date.strftime(expected_date, "%m/%d/%Y"))

        scheduler.make_crawler_requests()

        pass


if __name__ == '__main__':
    unittest.main()