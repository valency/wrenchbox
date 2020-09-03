# Wrenchbox for Python

A set of utilities for daily development.

本项目是一些常用的 Python 工具集合。

## Install

```shell
pip install wrenchbox
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

```
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

提供了多种多样的字典（dict）工具。

```python
from wrenchbox.dict import EnhancedDict
dict_a = {
    'a': 1,
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
print(EnhancedDict(dict_a).search('a')) # Search items with certain key
print(EnhancedDict(dict_a).merge(dict_b)) # Merge two dicts
print(EnhancedDict(dict_b).flatten()) # Flatten the dict and modify all nested keys into underscoped-connected form
print(EnhancedDict(dict_a).format(lambda x: x + 10, lambda x: x == 1)) # Format values of the dict through a filter
```

```json
{'a': 1, 'b': {'a': 1, 'b': {'a': 1, 'b': [{'a': 1, 'b': 2}, {'a': 1, 'b': {'a': 1, 'b': 2}}]}}}
{'a': 1, 'b': {'b': {'b': 2}}}
[1, 1, 1, 1, 1, 1]
{'a': 1, 'b': {'a': 1, 'b': {'a': 1, 'b': 2}}}
{'a': 1, 'b_b_b': 2}
{'a': 11, 'b': {'a': 11, 'b': {'a': 11, 'b': [{'a': 11, 'b': 2}, {'a': 11, 'b': {'a': 11, 'b': 2}}]}}}
```

### IO Handler

An advanced IO handerl providing various tools.

提供了多种多样的 IO 工具。

```
dd
```



### Snowflake Code Generator

生成若干 [Twitter Snowflake Codes](https://developer.twitter.com/en/docs/basics/twitter-ids)，原理和 [Go 版本](https://git.forchange.cn/framework/snowflake/)一致。

#### 使用方法：

Python 方式：

```python
from migrator.common.snowflake import Snowflake
print(next(Snowflake(twepoch=1483228800000).generate(31)))
```

命令行方式：
```shell
$ python3 -u -m migrator.common.snowflake -h
usage: snowflake.py [-h] [--debug] [--twepoch TWEPOCH] [--dc DC] -w W n

positional arguments:
  n                  # of results

optional arguments:
  -h, --help         show this help message and exit
  --debug            show debug information
  --twepoch TWEPOCH  twitter epoch, default: 1483228800000
  --dc DC            data center id, default: 31
  -w W               worker id
```

### YAML Config Reader

从 YAML 中读取一套配置文件。

#### 使用方法：

Python 方式：

```python
from migrator.common.config import Configuration
print(Configuration('migrator/uac/uac.yml', (0,1)))
```

命令行方式：

```shell
$ python3 -u -m migrator.common.config -h
usage: config.py [-h] [--debug] config

positional arguments:
  config      config file

optional arguments:
  -h, --help  show this help message and exit
  --debug     show debug information
```
