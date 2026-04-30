# 我的世界日志分析工具 (MC Log Analyzer)
基于 DeepSeek AI API 开发的可视化Minecraft日志自动分析工具，一键解析崩溃日志/服务端日志，快速定位模组冲突、配置错误、游戏崩溃原因，自动给出解决方案。


## 功能
- 可视化 GUI 界面
- 支持多 API 密钥管理（添加/删除/切换）
- 读取 Minecraft 崩溃日志、服务端日志
- AI 智能分析：精准定位崩溃原因
- 纯文本展示结果
- 本地配置保存，无需重复输入 API

## 运行前提
### 1. 获取 API 密钥
前往 [DeepSeek 平台](https://www.deepseek.com/) 注册并获取 API Key


### 2. 使用步骤
1. 在「API 管理」区域输入你的DeepSeek API ，点击**保存 API**
2. 从下拉框选择已保存的 API
3. 点击**选择日志文件**，上传 Minecraft 日志
4. 点击**开始分析日志**，等待 AI 分析完成
5. 在结果区域查看**崩溃原因**


## 配置说明
- 配置文件：`mc_log_analyzer_config.json`
- 作用：自动保存你的 API 密钥，本地存储，不会上传到任何服务器


## 注意事项
1. 确保网络可以正常访问 DeepSeek API
2. 日志内容过大会自动截取最后 8000 字符分析，避免请求超时
3. API Key 仅保存在本地配置文件，请注意保管
4. 若出现超时，可重试一次或检查网络状态


## 技术说明
- UI框架：Tkinter
- AI模型：deepseek
- 请求方式：HTTPS API 调用
