import requests
from datetime import datetime
import os

WEEKDAY_MAP = ['周一', '周二', '周三', '周四', '周五', '周六']
OUTPUT_FILE = "vaccine_schedule.md"

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

    return '\n'.join(lines)


def main():
    data = get_data()
    fetch_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    md_content = convert_to_markdown(data, fetch_time)

    # 添加预约链接
    md_content += '\n\n<a href="http://yfzweb.ishequ.net/#/login">疫苗接种预约</a>\n'

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ Markdown file saved to {OUTPUT_FILE}")



if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    main()
