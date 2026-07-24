# Jakana Python Ecosystem Reference

Jakana provides seamless access to the entire Python ecosystem through its intuitive `use <module>` syntax. By mapping directly to Python imports, Jakana enables you to leverage standard libraries and third-party packages without boilerplate. Every imported function is automatically qualified, keeping your code clean and readable.

## How It Works

When you import a module in Jakana:
`use math`

Jakana inspects the module and automatically qualifies its functions during transpilation. A call to `sqrt(16)` is transpiled to `math.sqrt(16)`. This behavior applies to ALL standard and third-party modules, allowing for concise syntax without polluting the global namespace.

## Categories

### 1. Mathematics & Statistics

- **math**: `sqrt`, `sin`, `cos`, `tan`, `log`, `exp`, `pi`, `e`, `floor`, `ceil`, `pow`, `radians`, `degrees`
- **statistics**: `mean`, `median`, `stdev`, `variance`
- **decimal**: `Decimal`, `getcontext`
- **fractions**: `Fraction`
- **cmath**: complex math operations

**Jakana Code:**
```jakana
use math
use statistics

data = [1, 2, 3, 4, 5]
avg = mean(data)
diff = sqrt(avg) + pi
echo diff
```

**Generated Python:**
```python
import math
import statistics

data = [1, 2, 3, 4, 5]
avg = statistics.mean(data)
diff = math.sqrt(avg) + math.pi
print(diff)
```

### 2. Data Structures & Algorithms

- **collections**: `Counter`, `defaultdict`, `OrderedDict`, `deque`, `namedtuple`
- **heapq**: `heappush`, `heappop`, `nlargest`, `nsmallest`
- **bisect**: `bisect_left`, `insort`
- **array**: `array`
- **queue**: `Queue`, `PriorityQueue`

**Jakana Code:**
```jakana
use collections
use heapq

counts = Counter(["a", "b", "a"])
q = []
heappush(q, 5)
heappush(q, 1)
echo heappop(q)
```

**Generated Python:**
```python
import collections
import heapq

counts = collections.Counter(["a", "b", "a"])
q = []
heapq.heappush(q, 5)
heapq.heappush(q, 1)
print(heapq.heappop(q))
```

### 3. String & Text Processing

- **string**: `ascii_letters`, `digits`, `punctuation`
- **re**: `search`, `match`, `findall`, `sub`, `compile`
- **textwrap**: `wrap`, `fill`, `dedent`
- **unicodedata**: `name`, `category`
- **difflib**: `SequenceMatcher`, `unified_diff`

**Jakana Code:**
```jakana
use re
use string

text = "Jakana 1.0!"
matches = findall("\w+", text)
echo digits
```

**Generated Python:**
```python
import re
import string

text = "Jakana 1.0!"
matches = re.findall("\w+", text)
print(string.digits)
```

### 4. File System & I/O

- **os**: `getcwd`, `listdir`, `mkdir`, `remove`, `rename`, `environ`
- **pathlib**: `Path`, `exists`, `glob`, `read_text`
- **shutil**: `copy`, `move`, `rmtree`
- **tempfile**: `mktemp`, `NamedTemporaryFile`
- **glob**: `glob`, `iglob`
- **io**: `StringIO`, `BytesIO`

**Jakana Code:**
```jakana
use os
use pathlib

cwd = getcwd()
p = Path("test.txt")
if exists(p) {
    echo read_text(p)
}
```

**Generated Python:**
```python
import os
import pathlib

cwd = os.getcwd()
p = pathlib.Path("test.txt")
if pathlib.exists(p):
    print(pathlib.read_text(p))
```

### 5. Date, Time & Calendar

- **datetime**: `datetime`, `date`, `time`, `timedelta`
- **time**: `time`, `sleep`, `perf_counter`
- **calendar**: `month`, `isleap`

**Jakana Code:**
```jakana
use datetime
use time

now = datetime.now()
sleep(1)
echo now
```

**Generated Python:**
```python
import datetime
import time

now = datetime.datetime.now()
time.sleep(1)
print(now)
```

### 6. JSON, CSV & Serialization

- **json**: `dumps`, `loads`, `dump`, `load`
- **csv**: `reader`, `writer`, `DictReader`
- **pickle**: `dumps`, `loads`
- **configparser**: `ConfigParser`
- **tomllib**: `loads`

**Jakana Code:**
```jakana
use json

data = {"lang": "Jakana", "fast": True}
encoded = dumps(data)
echo encoded
```

**Generated Python:**
```python
import json

data = {"lang": "Jakana", "fast": True}
encoded = json.dumps(data)
print(encoded)
```

### 7. Cryptography & Security

- **hashlib**: `sha256`, `md5`, `sha512`
- **hmac**: `new`, `digest`
- **secrets**: `token_hex`, `token_urlsafe`, `randbelow`
- **base64**: `b64encode`, `b64decode`
- **uuid**: `uuid4`, `uuid1`

**Jakana Code:**
```jakana
use hashlib
use secrets

token = token_hex(16)
hashed = sha256(token.encode()).hexdigest()
echo hashed
```

**Generated Python:**
```python
import hashlib
import secrets

token = secrets.token_hex(16)
hashed = hashlib.sha256(token.encode()).hexdigest()
print(hashed)
```

### 8. Networking & Web

- **urllib.parse**: `urlparse`, `urlencode`, `quote`
- **urllib.request**: `urlopen`
- **http.server**: `HTTPServer`
- **socket**: `socket`, `connect`
- **ipaddress**: `ip_address`, `ip_network`
- **ssl**: `create_default_context`
- **email**: `message_from_string`
- **html**: `escape`, `unescape`

**Jakana Code:**
```jakana
use urllib.parse
use html

url = urlparse("https://jakana.org?q=code")
safe = escape("<h1>Hello</h1>")
echo url.netloc
```

**Generated Python:**
```python
import urllib.parse
import html

url = urllib.parse.urlparse("https://jakana.org?q=code")
safe = html.escape("<h1>Hello</h1>")
print(url.netloc)
```

### 9. Concurrency & Parallelism

- **threading**: `Thread`, `Lock`, `Event`
- **multiprocessing**: `Process`, `Pool`
- **asyncio**: `run`, `gather`, `sleep`
- **subprocess**: `run`, `Popen`
- **queue**: `Queue`

**Jakana Code:**
```jakana
use subprocess
use threading

result = run(["echo", "hello"], capture_output=True)
echo result.stdout
```

**Generated Python:**
```python
import subprocess
import threading

result = subprocess.run(["echo", "hello"], capture_output=True)
print(result.stdout)
```

### 10. System & Platform

- **sys**: `argv`, `path`, `version`, `exit`
- **platform**: `system`, `node`, `release`, `machine`, `python_version`
- **os**: `environ`, `getpid`, `cpu_count`
- **signal**: `signal`, `SIGINT`
- **atexit**: `register`

**Jakana Code:**
```jakana
use sys
use platform

sys_name = system()
py_ver = python_version()
echo sys_name
```

**Generated Python:**
```python
import sys
import platform

sys_name = platform.system()
py_ver = platform.python_version()
print(sys_name)
```

### 11. Compression & Archives

- **zlib**: `compress`, `decompress`
- **gzip**: `open`, `compress`
- **bz2**: `compress`, `decompress`
- **zipfile**: `ZipFile`
- **tarfile**: `open`
- **lzma**: `compress`, `decompress`

**Jakana Code:**
```jakana
use zlib

data = b"hello world hello world"
compressed = compress(data)
echo decompress(compressed)
```

**Generated Python:**
```python
import zlib

data = b"hello world hello world"
compressed = zlib.compress(data)
print(zlib.decompress(compressed))
```

### 12. Functional Programming

- **itertools**: `chain`, `combinations`, `permutations`, `product`, `cycle`, `repeat`, `islice`, `groupby`
- **functools**: `reduce`, `partial`, `lru_cache`, `wraps`
- **operator**: `add`, `mul`, `itemgetter`, `attrgetter`

**Jakana Code:**
```jakana
use itertools
use functools

nums = [1, 2, 3]
pairs = combinations(nums, 2)
echo list(pairs)
```

**Generated Python:**
```python
import itertools
import functools

nums = [1, 2, 3]
pairs = itertools.combinations(nums, 2)
print(list(pairs))
```

### 13. Testing & Debugging

- **unittest**: `TestCase`
- **doctest**: `testmod`
- **pdb**: `set_trace`
- **timeit**: `timeit`
- **logging**: `info`, `warning`, `error`, `debug`
- **traceback**: `format_exc`, `print_exc`
- **warnings**: `warn`

**Jakana Code:**
```jakana
use logging

warning("This is a warning")
error("Critical failure")
```

**Generated Python:**
```python
import logging

logging.warning("This is a warning")
logging.error("Critical failure")
```

### 14. Introspection & Metaprogramming

- **inspect**: `getmembers`, `getsource`, `signature`
- **abc**: `ABC`, `abstractmethod`
- **dataclasses**: `dataclass`, `field`
- **typing**: `List`, `Dict`, `Optional`, `Union`
- **copy**: `copy`, `deepcopy`
- **pprint**: `pprint`

**Jakana Code:**
```jakana
use copy
use pprint

original = [1, [2, 3]]
cloned = deepcopy(original)
pprint(cloned)
```

**Generated Python:**
```python
import copy
import pprint

original = [1, [2, 3]]
cloned = copy.deepcopy(original)
pprint.pprint(cloned)
```

### 15. Third-Party Ecosystem (via pip)

Jakana natively integrates with external packages. You can utilize third-party modules seamlessly.

- **AI/ML**: `torch`, `tensorflow`, `transformers`, `sklearn`
- **Data**: `numpy`, `pandas`, `polars`, `scipy`
- **Web**: `requests`, `flask`, `fastapi`, `django`
- **Visualization**: `matplotlib`, `seaborn`, `plotly`
- **Scraping**: `beautifulsoup4` (bs4), `scrapy`, `selenium`
- **Database**: `sqlalchemy`, `pymongo`, `redis`
- **Cloud**: `boto3`, `google-cloud`
- **Image/Video**: `cv2` (opencv), `Pillow` (PIL)
- **NLP**: `spacy`, `nltk`
- **Automation**: `paramiko`, `fabric`, `ansible`

**Jakana Code (requests & numpy):**
```jakana
use requests
use numpy

res = get("https://api.github.com")
arr = array([1, 2, 3])
echo arr
```

**Generated Python:**
```python
import requests
import numpy

res = requests.get("https://api.github.com")
arr = numpy.array([1, 2, 3])
print(arr)
```

## Pipeline Operator with Ecosystem

Jakana's pipeline operator `|>` works naturally with functions from the ecosystem. It passes the output of the left expression as the first argument to the right function.

**Jakana Code:**
```jakana
use math
use statistics

[1.5, 2.3, 3.8] 
    |> mean
    |> ceil
    |> echo
```

**Generated Python:**
```python
import math
import statistics

print(math.ceil(statistics.mean([1.5, 2.3, 3.8])))
```
