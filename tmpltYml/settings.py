from functools import lru_cache
from os import path
from pprint import pprint

import yaml
from pydantic import BaseModel


class YamlConfigMixin:
    def read_yaml(self, config_filename):
        with open(path.join(self.path, config_filename)) as f:
            templates = yaml.safe_load(f)
        return templates


class Config(BaseModel, YamlConfigMixin):
    path: str = path.join(path.dirname(__file__), 'config')
    config: dict = dict()

    class Config:
        env_prefix = ""
        case_insensitive = True


@lru_cache()
def get_settings() -> Config:
    config = Config()
    templates = config.read_yaml('dev.yml')
    config.config = templates
    return config


if __name__ == '__main__':
    settings = get_settings()
    pprint(settings.config['service'])
    pprint(settings.config['database'])
