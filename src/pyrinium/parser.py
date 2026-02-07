import requests
import random
from .extractor import get_initial_data, get_livewire_token

XSRF_TOKEN_COOKIE_NAME = "XSRF-TOKEN"
SESSION_TOKEN_COOKIE_NAME = "raspisanie_universitet_sirius_session"
DEFAULT_TIMEOUT = 15


def get_call_method_update_object(method: str, params=None):
    """Build a Livewire update payload for a method call."""
    return {
        "type": "callMethod",
        "payload": {
            "id": format(int(random.random() + 1 * (36**10)), "010x")[2:],
            "method": method,
            "params": [] if params is None else params,
        },
    }


def get_events_array(data):
    """Extract events from raw Livewire response."""
    return data["serverMemo"]["events"]


class Parser:
    def __init__(
        self, base_url: str, main_grid_path: str, timeout: int = DEFAULT_TIMEOUT
    ):
        """Initialize low-level Livewire parser."""
        self.livewire_token = None
        self.session_token = None
        self.xsrf_token = None
        self.data = None

        self.base_url = base_url
        self.main_grid_path = main_grid_path
        self.timeout = timeout

        self.session = requests.Session()

    def _get_url(self, path):
        """Join base URL and API path."""
        return self.base_url + path

    def _sync_server_memo(self, response_data):
        """Update cached Livewire server memo from response."""
        self.data["serverMemo"]["data"].update(response_data["serverMemo"]["data"])
        self.data["serverMemo"]["checksum"] = response_data["serverMemo"]["checksum"]
        self.data["serverMemo"]["htmlHash"] = response_data["serverMemo"]["htmlHash"]

    def get_initial_data(self):
        """Load initial HTML, cookies and Livewire bootstrap data."""
        r = self.session.get(self.base_url, timeout=self.timeout)
        r.raise_for_status()
        html = r.text

        if (
            XSRF_TOKEN_COOKIE_NAME not in r.cookies
            or SESSION_TOKEN_COOKIE_NAME not in r.cookies
        ):
            raise Exception("CookieTokensError")

        self.xsrf_token = r.cookies.get(XSRF_TOKEN_COOKIE_NAME)
        self.session_token = r.cookies.get(SESSION_TOKEN_COOKIE_NAME)
        self.livewire_token = get_livewire_token(html)

        self.data = get_initial_data(html)

    def send_updates(self, updates):
        """Send update list to Livewire endpoint and return parsed JSON."""
        if self.data is None:
            raise RuntimeError(
                "Initial data is not loaded. Call get_initial_data() first."
            )

        headers = {"X-Livewire": "true", "X-Csrf-Token": self.livewire_token}

        r = self.session.post(
            self._get_url(self.main_grid_path),
            json={
                "fingerprint": self.data["fingerprint"],
                "serverMemo": self.data["serverMemo"],
                "updates": updates,
            },
            headers=headers,
            timeout=self.timeout,
        )
        r.raise_for_status()

        return r.json()

    def get_schedule(self, group):
        """Select group and return raw schedule response."""
        data = self.send_updates([get_call_method_update_object("set", [group])])

        return data

    def change_week(self, step):
        """Move week pointer by `step` and return the final raw response."""
        method = "addWeek" if step > 0 else "minusWeek"
        for i in range(abs(step)):
            data = self.send_updates([get_call_method_update_object(method)])

            self._sync_server_memo(data)
