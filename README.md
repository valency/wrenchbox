# Wrenchbox for Python

A set of utilities for daily development.

本项目是一些常用的 Python 工具集合。

## Install

```shell
pip install -U wrenchbox
```

## Usage

### Alert Hanlder

Send alerts to certain bots or web APIs.

通过钉钉机器人等渠道发送报警信息。

```shell
$ python3 -u -m wrenchbox.alert -h
usage: alert.py [-h] [--debug] --type TYPE [--token TOKEN] msg

positional arguments:
  msg                   the message

optional arguments:
  -h, --help            show this help message and exit
  --debug               show debug information
  --type TYPE, -p TYPE  alert type, must be "dingtalk"
  --token TOKEN, -k TOKEN
                        access token, if any
```

```python
from wrenchbox.alert import DingTalk
DingTalk('token').send('This is a warning message.')
```

```json
200
```

### Configuration Parser

Read a configuration from a YAML or JSON file.

从 YAML 或 JSON 中读取一段配置信息。

```shell
$ python3 -u -m wrenchbox.config -h
usage: config.py [-h] [--debug] config

positional arguments:
  config      config file

optional arguments:
  -h, --help  show this help message and exit
  --debug     show debug information
```

```python
from wrenchbox.config import Configuration
print(json.dumps(Configuration('wrenchbox/config.yml').__dict__, indent=2))
```

```json
{
  "version": 0,
  "name": "00000000-0000-0000-0000-000000000000",
  "config": {
    "key": "value",
    "nested": {
      "key": "value"
    },
    "list": [
      {
        "key": "value"
      },
      {
        "key": "value"
      }
    ]
  }
}
```

The following configurations will be automatically generated if not provided:

- `version` version of the configuration file, could be verified through `Configuration(version=(0,))`
- `worker` ID of the worker, default: 0

- `name` name of the worker, an [UUID](https://www.uuidgenerator.net/) will be generated if not provided

All configuration keys starting with `-` or `.` will be ignored (these keys should be used as audition only).

### Database Hanlder

An advanced database handler based on [SQLAlchemy](https://www.sqlalchemy.org/).

一个基于 [SQLAlchemy](https://www.sqlalchemy.org/) 开发的更简单的数据库处理模块。

```python
from wrenchbox.database import DatabaseHandler
DatabaseHandler({
    'test': 'sqlite:///test.db'
}, [
    ('test', 'test')
]).handle(
    'test', {
        'id': 1
    }, {
        'id': 1,
        'name': str(datetime.now())
    }, replace=True
)
```

The above code will insert or update a record with `id` = `1`.

### Datetime Hanlder

An advanced datetime handler based on [python-dateutil](https://pypi.org/project/python-dateutil/).

一个基于 [python-dateutil](https://pypi.org/project/python-dateutil/) 开发的更简单的日期和时间处理器。

```python
from wrenchbox.datetime import T
print(T().timestamp()) # Get timestamp
print(T().format()) # Format into YYYY-MM-DD HH:MM:SS
print(T().format('d')) # Format into YYYY-MM-DD
print(T().format('t')) # Format into HH:MM:SS
```

```
1598930603.003622
2020-09-01 11:23:23
2020-09-01
11:23:23
```

When initialising `T`, it is possible to pass the following arguments:

- `None` current timestamp will be generated
- `datetime.datetime` will be directly used
- `float` or `int` will be parsed as timestamp
- `str` will be parsed through [python-dateutil](https://pypi.org/project/python-dateutil/)

### Dictionary Hanlder

An advanced dictionary hander providing various tools.

提供了多种多样的字典（dict）处理工具。

```python
from wrenchbox.dict import EnhancedDict
dict_a = {
    'a': 'a',
    'b': {
        'a': 1,
        'b': {
            'a': 1,
            'b': [{
                'a': 1,
                'b': 2
            }, {
                'a': 1,
                'b': {
                    'a': 1,
                    'b': 2
                }
            }]
        }
    }
}
dict_b = {
    'a': 1,
    'b': {
        'b': {
            'b': 2
        }
    }
}
print(dict_a)
print(dict_b)
print(EnhancedDict(dict_a).search('a'))
print(EnhancedDict(dict_a).merge(dict_b))
print(EnhancedDict(dict_b).flatten())
print(EnhancedDict(dict_a).format(lambda x: x + 10, lambda x: isinstance(x, int)))
print(EnhancedDict(dict_a).remove_key('a'))
print(EnhancedDict(dict_a).remove_value(1))
```

```json
{"a": "a", "b": {"a": 1, "b": {"a": 1, "b": [{"a": 1, "b": 2}, {"a": 1, "b": {"a": 1, "b": 2}}]}}}
{"a": 1, "b": {"b": {"b": 2}}}
["a", 1, 1, 1, 1, 1]
{"a": 1, "b": {"a": 1, "b": {"a": 1, "b": 2}}}
{"a": 1, "b_b_b": 2}
{"a": "a", "b": {"a": 11, "b": {"a": 11, "b": [{"a": 11, "b": 12}, {"a": 11, "b": {"a": 11, "b": 12}}]}}}
{"b": {"b": {"b": [{"b": 2}, {"b": {"b": 2}}]}}}
{"a": "a", "b": {"b": {"b": [{"b": 2}, {"b": {"b": 2}}]}}}
```

### IO Handler

An advanced IO handerl providing various tools.

提供了多种多样的 IO 工具。

```python
from wrenchbox.io import BufferedWriter
w = BufferedWriter(buffer=50)
for i in range(100):
    w.write(i)    
w.close()
```

The above code will write two separate files with 50 records each.

### List Hanlder

An advanced list hander providing various tools.

提供了多种多样的列表（list）处理工具。

```python
from wrenchbox.list import EnhancedList
list_a = [1, [1, [2, 3], 2], 2]
print(list_a)
print(EnhancedList(list_a).flatten()) # Flatten the list and put all sub-lists into the root level
print(EnhancedList(list_a).pick(lambda x: x == 1)) # Pick values based on a function
print(EnhancedList(list_a).format(lambda x: x + 1, lambda x: isinstance(x, (int, float)))) # Format values of the list through a filter
```

```json
[1, [1, [2, 3], 2], 2]
[1, 1, 2, 3, 2, 2]
[1, [1]]
[[[2, 3], 2], 2]
[2, [2, [3, 4], 3], 3]
```

### Logging Tools

A series of tools for logging.

提供了美化的日志工具。

```python
from wrenchbox.logging import setup_log, progress
# Create a colorized logger and print logging messages
setup_log(level=logging.DEBUG, path='./log/', tag='wrenchbox')
logging.debug('This is a DEBUG message.')
logging.info('This is an INFO message.')
logging.warning('This is a WARNING message.')
logging.error('This is an ERROR message.')
logging.critical('This is an CRITICAL message.')
# Show a progress bar
for _i in range(100):
    progress(_i, 100)
    time.sleep(0.02)
```

```
[2020-09-28 10:18:40,084] This is a DEBUG message.
[2020-09-28 10:18:40,084] This is an INFO message.
[2020-09-28 10:18:40,084] This is a WARNING message.
[2020-09-28 10:18:40,085] This is an ERROR message.
[2020-09-28 10:18:40,085] This is an CRITICAL message.
[==========================================================--] 97.0%
```

Logs are colorized with the following default config:

```json
{
    DEBUG: "cyan",
    INFO: "green",
    WARNING: "yellow",
    ERROR: "red",
    CRITICAL: "magenta"
}
```

### Number Hanlder

An advanced number hander providing various tools.

提供了多种多样的数字（number）处理工具。

```python
from wrenchbox.number import EnhancedDecimal
print(EnhancedDecimal('3.1415926').round(Decimal('0.1'))) # Round a decimal with any unit like in excel
```

```json
3.1
```

### Object Tools

A series of objects for specific uses.

提供了一些杂项对象。

- `Dict2StrSafe`: a class that correctly converts `self.__dict__` to a JSON string without errors
- `Munch`: an alternative implementation of [Munch](https://github.com/Infinidat/munch)

### Snowflake Code Generator

Generate a series of [Twitter Snowflake Codes](https://developer.twitter.com/en/docs/basics/twitter-ids).

生成若干 [Twitter Snowflake Codes](https://developer.twitter.com/en/docs/basics/twitter-ids)。

```shell
$ python3 -u -m wrenchbox.snowflake -h
usage: snowflake.py [-h] [--debug] [--twepoch TWEPOCH] [-d D] -w W n

positional arguments:
  n                  # of results

optional arguments:
  -h, --help         show this help message and exit
  --debug            show debug information
  --twepoch TWEPOCH  twitter epoch, default: 1483228800000
  -d D               data center id, default: 31
  -w W               worker id, 0-31
```
```python
from wrenchbox.snowflake import Snowflake
print(next(Snowflake(twepoch=1483228800000).generate(31)))
```

```json
495059711868006400
```

### String Handler

An advanced string hander providing various tools.

提供了多种多样的字符串（string）处理工具。

```python
from wrenchbox.string import digits, random_chars, random_letters, random_numbers
print(digits(pi)) # Count the digits of a given float number
print(random_chars(3)) # Generate a random string from [a-zA-Z0-9]
print(random_letters(3)) # Generate a random string from [a-zA-Z]
print(random_numbers(3)) # Generate a random string from [0-9]
```

```
15
63f
FVK
007
```

### Text Handler

A set of advanced text processing modules.

提供了多种多样的文本处理工具。

```shell
$ python3 -u -m wrenchbox.text -h
usage: text.py [-h] [--debug] [--chinese] [-p P] f

positional arguments:
  f           file path

optional arguments:
  -h, --help  show this help message and exit
  --debug     show debug information
  --chinese   specify the input as Chinese
  -p P        part of speech to show, only works for Chinese
```

```python
from wrenchbox.text import S
print([i for i in S(open('test.txt', 'r').read()).v(chinese=True).words if i[1] in ('v',)])
```

```json
[("是", "v", 8), ("获取", "v", 1)]
```

