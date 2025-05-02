import json
import re

LIVEWIRE_TOKEN_REGEX = "window.livewire_token = '([0-9A-Za-z]+)';"
INITIAL_DATA_REGEX = "wire:initial-data=\"(.+)\""


def get_livewire_token(html: str):
    token = re.search(LIVEWIRE_TOKEN_REGEX, html)

    if token is None:
        raise Exception("LivewireTokenGettingError")

    return token[1]


def get_initial_data(html: str):
    raw_initial_data = re.search(INITIAL_DATA_REGEX, html)

    if raw_initial_data is None:
        raise Exception("InitialDataGettingError")

    initial_data_json = raw_initial_data[1].replace("&quot;", "\"")
    initial_data = json.loads(initial_data_json)

    return initial_data
