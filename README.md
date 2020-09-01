# Wrenchbox for Python

A set of utilities for daily development.

本项目是一些常用的 Python 工具集合。

## Install

```shell
pip install wrenchbox
```

## Usage

### Alert

Send alerts to certain bots or web APIs.

通过钉钉机器人等渠道发送报警信息。

```shell
$ python3 -u -m wrenchbox.alert -h                                                         usage: alert.py [-h] [--debug] --type TYPE [--token TOKEN] msg

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
$ python3 -u -m wrenchbox.config -h                                                       usage: config.py [-h] [--debug] config

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

### Datetime Parser

An advanced datetime parser based on [python-dateutil](https://pypi.org/project/python-dateutil/).

一个基于 [python-dateutil](https://pypi.org/project/python-dateutil/) 开发的更简单的日期和时间处理器。

```python
from wrenchbox.datetime import T
print(T().timestamp())
print(T().format())
print(T().format('d'))
print(T().format('t'))
```

```
1598930603.003622
2020-09-01 11:23:23
2020-09-01
11:23:23
```

