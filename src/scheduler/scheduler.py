import datetime

class Scheduler:
    
    def __init__(self, logger, request_handler) -> None:
        self.overview = []
        self.today = datetime.date.today()
        self.logger = logger
        self.request_handler = request_handler
        pass

    
    """
    JSON response
    [{"subreddit_names":"vlc",
      "date":"2022-07-26T11:59:25.071Z",
      "occurrence":1,
      "number_posts":0,
      "dataset_name":"jw_dataset_name",
      "request":{"subreddits":["vlc"],
                 "dataset_name":"jw_dataset_name",
                 "blacklist_comments":["bar"],
                 "blacklist_posts":["foo"],
                 "comment_depth":1,
                 "date_from":"07/23/2022",
                 "date_to":"07/24/2022",
                 "min_length_comments":5,
                 "min_length_posts":200,
                 "new_limit":100,
                 "post_selection":"new",
                 "replace_emojis":false,
                 "replace_urls":true}
    }]
    """
    def get_datasets(self):
        response = self.request_handler.get('https://feed-uvl.ifi.uni-heidelberg.de/hitec/repository/concepts/crawler_jobs/all')
        try:
            for entry in response.json():
                if entry["occurrence"] > 0:
                    date_of_entry = datetime.datetime.strptime(entry["date"][0:10], "%Y-%m-%d").date()
                    if (self.today-date_of_entry).days % entry["occurrence"] == 0:
                        self.overview.append(entry)
        except TypeError: 
            self.logger.info("No collections found")
        if len(self.overview) == 0:
            self.logger.info('No scheduled crawler tasks found!')
        else:
            self.logger.info('Jobs for scheduling:')
            self.logger.info(self.overview)
        pass

    def update_request_bodies(self):
        for index, entry in enumerate(self.overview):
            # adapte dates from original request to current dates
            self.overview[index]["request"]["date_to"] = datetime.date.strftime(self.today, "%m/%d/%Y")

            occurrence_days = entry["occurrence"]
            new_from_date = self.today + datetime.timedelta(days=-occurrence_days)
            self.overview[index]["request"]["date_from"] = datetime.date.strftime(new_from_date, "%m/%d/%Y")
            self.logger.info("Processing requests finished:")
            self.logger.info(self.overview)
        pass

    def make_crawler_requests(self):
        for entry in self.overview:
            request_body = entry["request"]
            response = self.request_handler.post('https://feed-uvl.ifi.uni-heidelberg.de/hitec/reddit/crawl', json=request_body)
            self.logger.info(f'Status Code: {response.status_code}')
            self.logger.info(request_body)
        pass

class AppReviewScheduler:
    
    def __init__(self, logger, request_handler) -> None:
        self.overview = []
        self.today = datetime.date.today()
        self.logger = logger
        self.request_handler = request_handler
        
    def get_datasets(self):
        response = self.request_handler.get('https://feed-uvl.ifi.uni-heidelberg.de/hitec/repository/concepts/app_review_crawler_jobs/all')
        try:
            for entry in response.json():
                if entry["app_occurrence"] > 0:
                    date_of_entry = datetime.datetime.strptime(entry["date"][0:10], "%Y-%m-%d").date()
                    if(self.today-date_of_entry). days % entry["app_occurrence"] == 0:
                        self.overview.append(entry)
        except TypeError:
            self.logger.info("No collections found")

        if len(self.overview) == 0:
            self.logger.info('No scheduled crawler tasks found!')
        else:
            self.logger.info('Jobs for scheduling:')
            self.logger.info(self.overview)
        pass
    
    def update_request_bodies(self):
        for index, entry in enumerate(self.overview):
            self.overview[index]["request"]["date_to"] = datetime.date.strftime(self.today, "%d/%m/%Y")
            
            occurrence_days = entry["app_occurrence"] 
            new_from_date = self.today + datetime.timedelta(days=-occurrence_days)
            self.overview[index]["request"]["date_from"] = datetime.date.strftime(new_from_date, "%d/%m/%Y")
            self.logger.info("Processing requests finished:")
            self.logger.info(self.overview)
        pass
            
    def make_crawler_requests(self):
        for entry in self.overview:
            request_body = entry["request"]
            response = self.request_handler.post('https://feed-uvl.ifi.uni-heidelberg.de/hitec/app/crawl', json=request_body)
            self.logger.info(f'Status Code: {response.status_code}')
            self.logger.info(request_body)
        pass