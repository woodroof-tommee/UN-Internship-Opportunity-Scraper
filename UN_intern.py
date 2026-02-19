import requests
import json
from datetime import datetime

BASE_API = "https://careers.un.org/rest/jobs"

def fetch_internships():
    params = {
        "language": "en",
        "jobType": "INT",  # Internship
        "page": 0,
        "size": 100
    }

    response = requests.get(BASE_API, params=params)
    response.raise_for_status()

    data = response.json()

    internships = []

    for job in data.get("jobs", []):
        internships.append({
            "title": job.get("jobTitle"),
            "job_id": job.get("jobId"),
            "department": job.get("department"),
            "location": job.get("dutyStation"),
            "posted": job.get("postingDate"),
            "deadline": job.get("expiryDate"),
            "url": f"https://careers.un.org/lbw/jobdetail.aspx?id={job.get('jobId')}"
        })

    return internships


def save_json(data):
    with open("internships.json", "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": datetime.utcnow().isoformat(),
            "count": len(data),
            "data": data
        }, f, indent=2)


def main():
    internships = fetch_internships()
    save_json(internships)
    print(f"Saved {len(internships)} internships.")


if __name__ == "__main__":
    main()
