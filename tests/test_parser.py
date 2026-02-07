from requests.cookies import RequestsCookieJar

from pyrinium.parser import Parser


class FakeResponse:
    def __init__(self, *, text="", json_data=None, cookies=None):
        self.text = text
        self._json_data = json_data or {}
        self.cookies = cookies or RequestsCookieJar()

    def raise_for_status(self):
        return None

    def json(self):
        return self._json_data


def _build_initial_html():
    return (
        "<html><head><script>"
        "window.livewire_token = 'TOKEN123';"
        "</script></head>"
        "<body>"
        '<div wire:initial-data="{&quot;fingerprint&quot;:{&quot;id&quot;:&quot;abc&quot;},'
        '&quot;serverMemo&quot;:{&quot;data&quot;:{},&quot;checksum&quot;:&quot;chk0&quot;}}"></div>'
        "</body></html>"
    )


def test_get_initial_data_loads_tokens_and_bootstrap():
    parser = Parser("https://example.com", "/livewire")

    cookies = RequestsCookieJar()
    cookies.set("XSRF-TOKEN", "xsrf-token")
    cookies.set("raspisanie_universitet_sirius_session", "session-token")
    parser.session.get = lambda *args, **kwargs: FakeResponse(
        text=_build_initial_html(), cookies=cookies
    )

    parser.get_initial_data()

    assert parser.xsrf_token == "xsrf-token"
    assert parser.session_token == "session-token"
    assert parser.livewire_token == "TOKEN123"
    assert parser.data["fingerprint"]["id"] == "abc"


def test_send_updates_requires_initial_data():
    parser = Parser("https://example.com", "/livewire")

    try:
        parser.send_updates([])
        assert False, "send_updates should raise without get_initial_data"
    except RuntimeError as exc:
        assert "Call get_initial_data() first" in str(exc)


def test_get_schedule_syncs_server_memo():
    parser = Parser("https://example.com", "/livewire")
    parser.livewire_token = "TOKEN"
    parser.data = {
        "fingerprint": {"id": "fingerprint"},
        "serverMemo": {"data": {"group": "old"}, "checksum": "old", "htmlHash": "h0"},
    }

    response_payload = {
        "serverMemo": {"data": {"group": "G1"}, "checksum": "new", "htmlHash": "h1"}
    }
    parser.session.post = lambda *args, **kwargs: FakeResponse(
        json_data=response_payload
    )

    result = parser.get_schedule("G1")

    assert result == response_payload
    assert parser.data["serverMemo"] == response_payload["serverMemo"]


def test_change_week_returns_final_response_and_syncs_state(monkeypatch):
    parser = Parser("https://example.com", "/livewire")
    parser.data = {
        "fingerprint": {"id": "fingerprint"},
        "serverMemo": {"data": {"week": 0}, "checksum": "chk0", "htmlHash": "h0"},
    }

    responses = [
        {"serverMemo": {"data": {"week": 1}, "checksum": "chk1", "htmlHash": "h1"}},
        {"serverMemo": {"data": {"week": 2}, "checksum": "chk2", "htmlHash": "h2"}},
    ]

    def fake_send_updates(_updates):
        return responses.pop(0)

    monkeypatch.setattr(parser, "send_updates", fake_send_updates)

    result = parser.change_week(2)

    assert result["serverMemo"]["data"]["week"] == 2
    assert parser.data["serverMemo"]["data"]["week"] == 2


def test_change_week_step_zero_returns_current_state():
    parser = Parser("https://example.com", "/livewire")
    parser.data = {"fingerprint": {"id": "fp"}, "serverMemo": {"data": {"week": 0}}}

    assert parser.change_week(0) == parser.data
