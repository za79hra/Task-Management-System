from app.database.mongodb import mongo_db
from datetime import datetime
import csv


def generate_user_report(user_id: int, to_file: bool = False):
    """
    تولید گزارش برای یک کاربر مشخص
    """
    tasks_collection = mongo_db.get_collection("tasks")
    tasks = list(tasks_collection.find({"user_id": user_id}))

    done_tasks = len([task for task in tasks if task["status"] == "done"])
    in_progress_tasks = len([task for task in tasks if task["status"] == "in_progress"])
    new_tasks = len([task for task in tasks if task["status"] == "new"])

    report = {
        "user_id": user_id,
        "done_tasks": done_tasks,
        "in_progress_tasks": in_progress_tasks,
        "new_tasks": new_tasks,
        "total_tasks": len(tasks)
    }

    if to_file:
        with open(f"reports/user_{user_id}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(report.keys())
            writer.writerow(report.values())

    return report


def generate_project_report():
    """
    تولید گزارش کلی پروژه
    """
    tasks_collection = mongo_db.get_collection("tasks")
    tasks = list(tasks_collection.find())

    done_tasks = len([task for task in tasks if task["status"] == "done"])
    in_progress_tasks = len([task for task in tasks if task["status"] == "in_progress"])
    new_tasks = len([task for task in tasks if task["status"] == "new"])

    report = {
        "done_tasks": done_tasks,
        "in_progress_tasks": in_progress_tasks,
        "new_tasks": new_tasks,
        "total_tasks": len(tasks)
    }

    return report
