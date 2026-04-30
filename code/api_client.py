from openai import OpenAI
from openai import APIError, APITimeoutError, APIConnectionError
from config import DEEPSEEK_BASE_URL, MODEL_NAME, REQUEST_TIMEOUT

class APIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        #初始化官方SDK客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=DEEPSEEK_BASE_URL,
            timeout=REQUEST_TIMEOUT
        )
    def analyze_log(self, log_content, stream=False, enable_thinking=False):
        prompt = "请你分析Minecraft日志"
        messages = [{"role": "user", "content": prompt + log_content}]
        extra_body = {}

        #开关深度思考
        if enable_thinking:
            extra_body["thinking"] = {"type": "enabled"}
        else:
            extra_body["thinking"] = {"type": "disabled"}

        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.1,
                stream=stream,
                extra_body=extra_body
            )
            if stream:
                return response, None
            else:
                return response.choices[0].message.content, None
        except APITimeoutError:
            return None, "请求超时！AI服务器响应超过90秒，请重试或检查网络。"
        except APIConnectionError:
            return None, "连接失败！请检查网络或API地址配置。"
        except APIError as e:
            return None, f"API错误：{str(e)}"
        except Exception as e:
            return None, f"未知错误：{str(e)}"