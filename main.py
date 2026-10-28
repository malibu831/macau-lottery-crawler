"""
澳门特码/六合预测数据采集器
支持自动轮询今日多算法推荐、历史归档索引与结构化字段提取。
"""

import requests
import json
import xml.etree.ElementTree as ET

# 目标数据源（请替换为你绑定的真实域名）
TARGET_DOMAIN = "https://blackcat8.com/"

def fetch_today():
    """通过 /today 接口获取今日最新精选预测"""
    url = f"{TARGET_DOMAIN}/today"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        resp = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        if resp.status_code == 200:
            print(f"[+] 成功抓取今日数据，落地URL: {resp.url}")
            return resp.text
        print(f"[-] 请求失败，状态码: {resp.status_code}")
    except Exception as e:
        print(f"[!] 抓取异常: {e}")
    return None

def fetch_rss():
    """解析每日多门派精算 RSS 订阅流"""
    url = f"{TARGET_DOMAIN}/rss.xml"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            items = []
            for item in root.findall(".//item"):
                title = item.find("title").text if item.find("title") is not None else ""
                link = item.find("link").text if item.find("link") is not None else ""
                desc = item.find("description").text if item.find("description") is not None else ""
                items.append({"title": title, "link": link, "desc": desc})
            print(f"[+] RSS 解析成功，共获取 {len(items)} 条算法数据")
            return items
    except Exception as e:
        print(f"[!] RSS 解析异常: {e}")
    return []

if __name__ == "__main__":
    print("[*] 正在同步今日预测数据...")
    fetch_today()
    print("[*] 正在解析多门派算法通道...")
    records = fetch_rss()
    for r in records[:3]:
        print(f" -> {r['title']}")
