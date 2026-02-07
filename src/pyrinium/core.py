from .parser import Parser


def prettify_schedule(response):
    """Convert raw Livewire response into a compact schedule payload."""
    data = response["serverMemo"]["data"]

    result = {
        "group": data["group"],
        "events": [x for i in data["events"] for x in data["events"][i]]
        if "events" in data
        else [],
    }

    return result


class Pyrinium:
    def __init__(
        self,
        base_url="https://schedule.siriusuniversity.ru",
        main_grid_path="/livewire/message/main-grid",
        timeout=15,
    ):
        """Create a client for Sirius University schedule.

        Args:
            base_url: Main website URL.
            main_grid_path: Livewire endpoint path.
            timeout: Request timeout in seconds.
        """
        self.parser = Parser(base_url, main_grid_path, timeout=timeout)

    def get_initial_data(self):
        """Load initial page state, cookies and Livewire token.

        Must be called before any schedule operations.
        """
        self.parser.get_initial_data()

        return True

    def get_schedule(self, group: str):
        """Fetch schedule for a group.

        Args:
            group: Group name, for example "К0609-24".

        Returns:
            Dict with fields:
            - group: selected group name.
            - events: flat list of events.
        """
        schedule = self.parser.get_schedule(group)

        return prettify_schedule(schedule)

    def change_week(self, step: int):
        """Move schedule window by week offset.

        Args:
            step: Number of weeks to move.
                Positive value moves forward.
                Negative value moves backward.
                Zero keeps current week.

        Returns:
            Raw Livewire response of the final step, or current state for step=0.
        """
        return self.parser.change_week(step)
