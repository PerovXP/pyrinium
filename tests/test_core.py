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
