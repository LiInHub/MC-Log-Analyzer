import os

#配置文件路径
CONFIG_PATH = "mc_log_analyzer_config.json"

#AI API 接口配置
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"
REQUEST_TIMEOUT = 90
LOG_MAX_LENGTH = 8000  #截取日志最后长度