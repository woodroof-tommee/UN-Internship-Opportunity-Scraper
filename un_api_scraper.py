from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_un_jobs():
    url = "https://careers.un.org/lbw/home.aspx?viewtype=ip"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for job in soup.find_all("a", class_="jobtitle"):
        jobs.append({
            "title": job.text.strip(),
            "link": "https://careers.un.org" + job["href"]
        })

    return jobs

@app.route("/")
def home():
    return "UN Internship API is running!"

@app.route("/jobs")
def get_jobs():
    data = scrape_un_jobs()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
