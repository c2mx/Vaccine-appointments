import requests
from datetime import datetime, timedelta, timezone
import os
import markdown
from pathlib import Path

WEEKDAY_MAP = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
OUTPUT_MD = "README.md"
OUTPUT_HTML = "index.html"

def get_data():
    url = "http://yfzweb.ishequ.net/njf3322/Cl/MobliePreventInfo/searchareatime"
    params = {
        "fyuuid": "9657841792114edc8ba054d1ec77b24e",
        "arealevel": "00YJ",
        "pagesize": 20
    }
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json().get('detail', [])
    except Exception as e:
        print("Error fetching data:", e)
        return []

def convert_to_markdown(data, fetch_time):
    lines = []
    lines.append("# 🗓️ 沿江疫苗预约情况\n")
    lines.append(f"> 数据抓取时间：{fetch_time}\n")
    lines.append("| 日期 | 星期 | 总数 | 剩余 |")
    lines.append("|------|------|------|------|")

    for item in data:
        date_str = item.get('maketimes')
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            weekday = WEEKDAY_MAP[date_obj.weekday()]
        except:
            weekday = "未知"

        total = item.get('amjoindoor', 0)
        joined = item.get('amindoor', 0)
        remain = total - joined

        # 高亮周六
        if weekday == '周六':
            line = f"| **{date_str}** | **{weekday}** | **{total}** | **{remain}** |"
        else:
            line = f"| {date_str} | {weekday} | {total} | {remain} |"

        lines.append(line)

    lines.append('\n\n<div class="button-container">\n<a class="btn" href="http://yfzweb.ishequ.net/#/login" target="_blank">立即预约疫苗接种</a>\n</div>\n')


    return '\n'.join(lines)

def convert_markdown_to_html(md_content):
    body = markdown.markdown(md_content, extensions=["fenced_code", "tables"])
    css = """
    <style>
    body {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        background-color: #f9f9f9;
        color: #333;
        max-width: 860px;
        margin: 40px auto;
        padding: 20px;
        line-height: 1.6;
    }
    h1 {
        color: #2c3e50;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 8px;
        text-align: center;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    blockquote {
        color: #555;
        margin: 20px 0;
        padding-left: 10px;
        border-left: 4px solid #ccc;
        background: #fefefe;
    }
    a {
        color: #007acc;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    .button-container {
        text-align: center;
        margin-top: 30px;
    }
    .btn {
        display: inline-block;
        background-color: #28a745;
        color: white;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        text-decoration: none;
        transition: background-color 0.3s ease;
    }
    .btn:hover {
        background-color: #218838;
    }
    </style>
    """
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>沿江疫苗预约情况</title>
    {css}
</head>
<body>
{body}
</body>
</html>"""
    return html

def main():
    data = get_data()
    CST = timezone(timedelta(hours=8))
    fetch_time = datetime.now(CST).strftime("%Y年%m月%d日 %H:%M （北京时间）")
    md_content = convert_to_markdown(data, fetch_time)

    # 写入 Markdown 文件
    Path(OUTPUT_MD).write_text(md_content, encoding="utf-8")
    print(f"✅ Markdown file saved to {OUTPUT_MD}")

    # 转换并写入 HTML 文件
    html_content = convert_markdown_to_html(md_content)
    Path(OUTPUT_HTML).write_text(html_content, encoding="utf-8")
    print(f"✅ HTML file saved to {OUTPUT_HTML}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
