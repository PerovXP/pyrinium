from src.pyrinium.parser.core import Parser


def prettify_schedule(response):
    data = response["serverMemo"]["data"]

    result = {
        "group": data["group"],
        "events": [x for i in data["events"] for x in data["events"][i]] if "events" in data else []
    }

    return result


class Pyrinium:
    def __init__(self, base_url="https://schedule.siriusuniversity.ru", main_grid_path="/livewire/message/main-grid"):
        self.parser = Parser(base_url, main_grid_path)

    def get_initial_data(self):
        self.parser.get_initial_data()

        return True

    def get_schedule(self, group: str):
        schedule = self.parser.get_schedule(group)

        return prettify_schedule(schedule)

    def change_week(self, step: int):
        return self.parser.change_week(step)
