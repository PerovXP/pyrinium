![Pyrinium](https://raw.githubusercontent.com/PerovXP/pyrinium/main/assets/banner.png)

# Pyrinium

Pyrinium is a small Python client for reading Sirius University schedule data.

It exposes a compact public API and emulates the schedule website's Livewire
requests under the hood.

## Status

Pyrinium is currently in beta.

The public Python API is intentionally small and expected to stay stable. The
package depends on an unofficial Livewire interface used by the upstream
website, so website-side protocol changes may require package updates.

## Installation

```bash
pip install pyrinium
```

## Usage

```python
from pyrinium import Pyrinium

client = Pyrinium()
client.get_initial_data()

schedule = client.get_schedule("К0609-24")

print(schedule["group"])
print(schedule["events"])
```

## Change Week

```python
from pyrinium import Pyrinium

client = Pyrinium()
client.get_initial_data()

client.get_schedule("К0609-24")
next_week = client.change_week(1)

previous_week = client.change_week(-1)
```

## API

### `Pyrinium.get_initial_data()`

Loads the initial page state, cookies, and Livewire token. Call this before
schedule operations.

### `Pyrinium.get_schedule(group: str)`

Fetches the schedule for a group.

Returns:

```python
{
    "group": "К0609-24",
    "events": [...]
}
```

### `Pyrinium.change_week(step: int)`

Moves the schedule window by week offset.

- positive values move forward
- negative values move backward
- zero keeps the current week

Returns the same compact schedule format as `get_schedule()`.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

pytest
python -m build
twine check dist/*
```

## License

MIT
