import requests
from config import ApiConfig, PROJECTS


class BatchQueryError(Exception):
    pass


def fetch_board_summary() -> dict:
    url = ApiConfig.batch_query_url()
    payload = {"projects": PROJECTS}

    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise BatchQueryError(f"请求 batch-query 接口失败: {e}")

    data = resp.json()
    board_summary = data.get("board_summary")
    if not board_summary:
        raise BatchQueryError("响应中未找到 board_summary 字段")

    return board_summary


def format_beat_rate_sms(board_summary: dict) -> str:
    lines = []

    assembly = board_summary.get("assembly")
    if assembly:
        beat = assembly.get("beat_rate", "N/A")
        anomaly = assembly.get("anomaly_rate", "N/A")
        lines.append(f"[总成组装] 节拍兑现率: {beat}% 异常工序占比: {anomaly}%")

    delivery = board_summary.get("commissioning")
    if delivery:
        beat = delivery.get("beat_rate", "N/A")
        anomaly = delivery.get("anomaly_rate", "N/A")
        lines.append(f"[调试交付] 节拍兑现率: {beat}% 异常工序占比: {anomaly}%")

    return "; ".join(lines) if lines else ""
