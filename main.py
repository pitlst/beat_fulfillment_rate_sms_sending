from config import DatabaseConfig
from database import insert_one
from api_client import fetch_board_summary, format_beat_rate_sms, BatchQueryError

TABLE = "massage.dbo.sms_send"


def main():
    try:
        DatabaseConfig.validate()
    except ValueError as e:
        print(f"配置错误: {e}")
        print("请复制 .env.example 为 .env 并填写数据库连接信息")
        return

    try:
        board_summary = fetch_board_summary()
    except BatchQueryError as e:
        print(f"获取看板数据失败: {e}")
        return

    content = format_beat_rate_sms(board_summary)
    if not content:
        print("未能从看板数据中提取到有效信息，跳过插入")
        return

    print(f"短信内容: {content}")

    result = insert_one(
        table=TABLE,
        data={
            "SendPhone": "13800138000",
            "SendContent": content,
            "SendState": 0,
            "Senddefault": "",
        },
    )
    print(f"插入成功，影响行数: {result}")


if __name__ == "__main__":
    main()
