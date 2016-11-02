# jBHTrans
Python script to check bus locations in Belo Horizonte - Brazil.

Requires BeautifulSoup 4 and Requests, you can install them with pip:

```bash
[sudo] pip install bs4
```

```bash
[sudo] pip install requests
```

## Usage

There are two main methods: `getAvailableBusLines` and `getBusLocations`. The former returns all available bus lines and the latter returns all available bus locations for a line.

Example:

```python
from jBHTrans import jBHTrans

j = jBHTrans()
lines = j.getAvailableBusLines()
locations = j.getBusLocations(lineNumber=lines[0]["lineNumber"], lineName=lines[0]["lineName"])
```
