import datetime

class Scheduler:
    
    def __init__(self) -> None:
        self.overview = []
        self.today = datetime.date.today()
        pass

    def set_datasets(self, dataset):
        for entry in dataset:
            if entry["occurrence"] > 0:
                self.overview.append(entry)
        pass

    def get_updated_request_body(self):
        for entry in self.overview:
            # adapte dates from original request to current dates
            entry["request"]["to_date"] = datetime.date.strftime(self.today, "%m/%d/%Y")

            occurrence_days = entry["occurrence"]
            new_from_date = self.today + datetime.timedelta(days=-occurrence_days)
            entry["request"]["to_date"] = datetime.date.strftime(new_from_date, "%m/%d/%Y")

        return self.overview
            