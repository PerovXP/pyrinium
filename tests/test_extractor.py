from pyrinium.extractor import get_initial_data


def test_extractor_parses_initial_data_from_attribute_only():
    html = (
        '<div wire:initial-data="{&quot;fingerprint&quot;:{&quot;id&quot;:&quot;x&quot;},'
        '&quot;serverMemo&quot;:{&quot;data&quot;:{&quot;k&quot;:1}}}" class="x"></div>'
    )

    result = get_initial_data(html)

    assert result["fingerprint"]["id"] == "x"
    assert result["serverMemo"]["data"]["k"] == 1
