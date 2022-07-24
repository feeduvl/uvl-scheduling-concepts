import datetime

class Scheduler:
    
    def __init__(self, logger, request_handler) -> None:
        self.overview = []
        self.today = datetime.date.today()
        self.logger = logger
        self.request_handler = request_handler
        pass

    def get_datasets(self):
        response = self.request_handler.get('https://feed-uvl.ifi.uni-heidelberg.de/hitec/repository/concepts/crawler_jobs/all')
        for entry in response.json():
            if entry["occurrence"] > 0:
                self.overview.append(entry)
        if len(self.overview) == 0:
            self.logger.info('No scheduled crawler tasks found!')
        pass

    def update_request_bodies(self):
        for index, entry in enumerate(self.overview):
            # adapte dates from original request to current dates
            self.overview[index]["request"]["date_to"] = datetime.date.strftime(self.today, "%m/%d/%Y")

            occurrence_days = entry["occurrence"]
            new_from_date = self.today + datetime.timedelta(days=-occurrence_days)
            self.overview[index]["request"]["date_from"] = datetime.date.strftime(new_from_date, "%m/%d/%Y")
        pass

    def make_crawler_requests(self):
        for entry in self.overview:
            request_body = entry["request"]
            print(request_body)
            response = self.request_handler.post('https://feed-uvl.ifi.uni-heidelberg.de/hitec/reddit/crawl', json=request_body)
            self.logger.info(f'Status Code: {response.status_code}')
            self.logger.info(request_body)
        pass

            