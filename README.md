![Pyrinium](https://raw.githubusercontent.com/PerovXP/pyrinium/main/assets/banner.png)

## Installation

`pip install pyrinium`

## Usage

```python
from pyrinium import Pyrinium

c = Pyrinium()

c.get_initial_data() # Required
print(c.get_schedule("К0609-24"))
```

## How it works

Module emulates user interactions with schedule. Written using reverse
engineering tricks.

## License

MIT Licensed
