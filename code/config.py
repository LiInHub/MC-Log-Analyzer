import os

# 获取main.py所在目录（兼容不同运行场景）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 配置文件路径 - 改为Data文件夹下的AI_api_config.json
CONFIG_PATH = os.path.join(BASE_DIR, "Data", "AI_api_config.json")

# AI API 接口配置
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"
REQUEST_TIMEOUT = 90
LOG_MAX_LENGTH = 8000  # 截取日志最后长度