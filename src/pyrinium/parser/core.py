import requests
import random

XSRF_TOKEN_COOKIE_NAME = "XSRF-TOKEN"
SESSION_TOKEN_COOKIE_NAME = "raspisanie_universitet_sirius_session"


def get_call_method_update_object(method: str, params=None):
    return {
        "type": "callMethod",
        "payload": {
            "id": format(int(random.random() + 1 * (36 ** 10)), "010x")[2:],
            "method": method,
            "params": [] if params is None else params
        }
    }


def get_events_array(data):
    return data["serverMemo"]["events"]


class Parser:
    def __init__(self, base_url: str, main_grid_path: str):
        self.livewire_token = None
        self.session_token = None
        self.xsrf_token = None
        self.data = None

        self.base_url = base_url
        self.main_grid_path = main_grid_path

        self.session = requests.Session()

    def get_url(self, path):
        return self.base_url + path

    def get_initial_data(self):
        r = self.session.get(self.base_url)
        html = r.text

        if XSRF_TOKEN_COOKIE_NAME not in r.cookies or SESSION_TOKEN_COOKIE_NAME not in r.cookies:
            raise Exception("CookieTokensError")

        self.xsrf_token = r.cookies.get(XSRF_TOKEN_COOKIE_NAME)
        self.session_token = r.cookies.get(SESSION_TOKEN_COOKIE_NAME)
        self.livewire_token = get_livewire_token(html)

        self.data = get_initial_data(html)

    def send_updates(self, updates):
        headers = {
            "X-Livewire": "true",
            "X-Csrf-Token": self.livewire_token
        }

        r = self.session.post(
            self.get_url(self.main_grid_path),
            json={
                "fingerprint": self.data["fingerprint"],
                "serverMemo": self.data["serverMemo"],
                "updates": updates
            },
            headers=headers
        )

        return r.json()

    def get_schedule(self, group):
        data = self.send_updates([get_call_method_update_object("set", [group])])

        return data

    def change_week(self, step):
        method = "addWeek" if step > 0 else "minusWeek"
        for i in range(abs(step)):
            data = self.send_updates([get_call_method_update_object(method)])

            self.data["serverMemo"]["data"].update(data["serverMemo"]["data"])
            self.data["serverMemo"]["checksum"] = data["serverMemo"]["checksum"]
            self.data["serverMemo"]["htmlHash"] = data["serverMemo"]["htmlHash"]
