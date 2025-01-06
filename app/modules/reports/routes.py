from fastapi import APIRouter, Depends
from app.modules.reports.services import generate_user_report, generate_project_report
from fastapi.responses import JSONResponse, FileResponse

report_router = APIRouter()

@report_router.get("/user/{user_id}")
def user_report(user_id: int):
    """
    دریافت گزارش وظایف یک کاربر
    """
    report = generate_user_report(user_id)
    return JSONResponse(content=report)

@report_router.get("/project")
def project_report():
    """
    دریافت گزارش کلی پروژه
    """
    report = generate_project_report()
    return JSONResponse(content=report)

@report_router.get("/download/{user_id}")
def download_user_report(user_id: int):
    """
    دانلود گزارش یک کاربر به صورت CSV
    """
    file_path = f"reports/user_{user_id}.csv"
    generate_user_report(user_id, to_file=True)
    return FileResponse(file_path, media_type="text/csv", filename=f"user_{user_id}_report.csv")
