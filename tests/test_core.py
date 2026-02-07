from pyrinium.core import Pyrinium


def test_pyrinium_get_schedule_returns_prettified_events():
    client = Pyrinium()
    client.parser.get_schedule = lambda _group: {
        "serverMemo": {
            "data": {
                "group": "К0609-24",
                "events": {
                    "2026-02-01": [{"name": "Математика"}],
                    "2026-02-02": [{"name": "Физика"}],
                },
            }
        }
    }

    result = client.get_schedule("К0609-24")

    assert result["group"] == "К0609-24"
    assert result["events"] == [{"name": "Математика"}, {"name": "Физика"}]


def test_pyrinium_change_week_returns_prettified_payload():
    client = Pyrinium()
    client.parser.change_week = lambda _step: {
        "serverMemo": {
            "data": {
                "group": "К0609-24",
                "events": {
                    "2026-02-01": [{"name": "Математика"}],
                    "2026-02-02": [{"name": "Физика"}],
                },
            }
        }
    }

    result = client.change_week(1)

    assert result == {
        "group": "К0609-24",
        "events": [{"name": "Математика"}, {"name": "Физика"}],
    }


def test_pyrinium_change_week_without_group_does_not_fail():
    client = Pyrinium()
    client.parser.change_week = lambda _step: {
        "serverMemo": {
            "data": {
                "events": {
                    "2026-02-01": [{"name": "Математика"}],
                },
            }
        }
    }

    result = client.change_week(1)

    assert result == {"group": None, "events": [{"name": "Математика"}]}
