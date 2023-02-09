import argparse
import os
import configparser
import time


class Config:
    def __init__(self, config_file="config.ini"):
        self._config = {
            "username": None,
            "password": None,
            "start_date": time.strftime("%Y-%m-%d", time.localtime()),
            "end_date": time.strftime("%Y-%m-%d", time.localtime()),
            "standard_output": True,
            "qianji": False,
        }

        self._set_from_config_file(config_file)
        self._set_from_env()
        self._set_from_args()

    def get(self, key: str):
        """
        `key` can be one of the following:
        - username
        - password
        - start_date
        - end_date
        - standard_output
        - qianji
        """
        return self._config[key]

    def set(self, key: str, value):
        """
        `key` can be one of the following:
        - username
        - password
        - start_date
        - end_date
        - standard_output
        - qianji
        """
        self._config[key] = value

    def _set_from_config_file(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        for i in config:
            for j in config[i]:
                if config[i][j] != "":
                    self._config[j] = (
                        config[i][j] if i != "options" else config[i].getboolean(j)
                    )

    def _set_from_env(self):
        self._config["username"] = os.environ.get(
            "WHUCF_USERNAME", self._config["username"]
        )
        self._config["password"] = os.environ.get(
            "WHUCF_PASSWORD", self._config["password"]
        )

    def _set_from_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-u",
            "--username",
            help="用户名",
            default=self._config["username"],
        )
        parser.add_argument(
            "-p",
            "--password",
            help="密码",
            default=self._config["password"],
        )
        parser.add_argument(
            "-s",
            "--start-date",
            help="起始日期，格式为YYYY-MM-DD，默认当天",
            default=self._config["start_date"],
        )
        parser.add_argument(
            "-e",
            "--end-date",
            help="终止日期，格式为YYYY-MM-DD，默认当天",
            default=self._config["end_date"],
        )
        parser.add_argument(
            "-o",
            "--standard_output",
            action="store_true",
            help="是否向标准输出打印结果",
            default=self._config["standard_output"],
        )
        parser.add_argument(
            "--qianji",
            action="store_true",
            help="是否输出到钱迹",
            default=self._config["qianji"],
        )
        self._config = vars(parser.parse_args())

    def __str__(self):
        return str(self._config)


if __name__ == "__main__":
    print(Config())
