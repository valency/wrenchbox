import argparse
import json
import logging
import uuid

import ruamel.yaml as yaml
from munch import Munch

from .logging import setup_log
from .object import Dict2StrSafe


class Configuration(Dict2StrSafe):
    def __init__(self, path: str, version: tuple = (0,)):
        """
        Create a configuration object
        :param path: the yaml or json file path
        :param version: accepted versions as a tuple
        """
        self.version = None
        self.worker = 0
        self.name = str(uuid.uuid4())
        with open(path) as f:
            data = f.read()
        if path.endswith('yml') or path.endswith('yaml'):
            data = yaml.safe_load(data)
        elif path.endswith('json'):
            data = json.loads(data)
        else:
            raise ValueError('config file must end with "yml", "yaml", or "json"')
        data = Munch(data)
        for i in data:
            if not i.startswith('_') or i.startswith('.'):
                setattr(self, i, data[i])
            else:
                logging.warning('Config key starts with "_" or "." will be ignored: {}'.format(i))
        if self.version is None:
            logging.warning('Configuration version is not set and may cause compatibility problems.')
        elif self.version not in version:
            raise ValueError('Version "{}" is not accepted, accepted versions: {}', self.version, ','.join(version))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', default=False, help='show debug information')
    parser.add_argument('config', type=str, help='config file')
    args, _ = parser.parse_known_args()
    setup_log(level=logging.DEBUG if args.debug else logging.INFO)
    print(json.dumps(Configuration(args.config).__dict__, indent=2))
