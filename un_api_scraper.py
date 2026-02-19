import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

# 爬取 UN 实习岗位的函数
def scrape_un_internships():
    url = "https://careers.un.org/lbw/home.aspx?viewtype=ip"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []
    # 简单示例：抓取岗位列表
    # 注意：根据 UN 官网结构调整
    for item in soup.select(".table-striped tbody tr"):
        title_tag = item.select_one("td a")
        if title_tag:
            jobs.append({
                "title": title_tag.get_text(strip=True),
                "link": "https://careers.un.org" + title_tag["href"]
            })
    return jobs

@app.route("/")
def index():
    return "UN Internship API is running!"

@app.route("/jobs")
def jobs():
    data = scrape_un_internships()
    return jsonify(data)

if __name__ == "__main__":
    # Render 免费版要求使用环境变量 PORT
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
