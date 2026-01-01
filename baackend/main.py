import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Report
from ai_matching import text_similarity, image_similarity

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/report")
async def create_report(
    type: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    contact: str = Form(...),
    image: UploadFile = None,
):

    db: Session = next(get_db())

    img_path = None
    if image:
        img_path = f"{UPLOAD_DIR}/{image.filename}"
        with open(img_path, "wb") as f:
            f.write(await image.read())

    report = Report(
        type=type,
        title=title,
        description=description,
        location=location,
        image_path=img_path,
        contact=contact,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    reports = db.query(Report).filter(Report.id != report.id).all()

    matches = []

    # text match
    texts = [r.description for r in reports]
    scores = text_similarity(report.description, texts)

    for idx, score in enumerate(scores):
        if score > 0.55:
            matches.append(reports[idx])

    # image match
    if report.image_path:
        for r in reports:
            if r.image_path:
                score = image_similarity(report.image_path, r.image_path)
                if score > 0.55:
                    matches.append(r)

    return {
        "saved": True,
        "report": report.id,
        "matches": [
            {
                "id": m.id,
                "type": m.type,
                "title": m.title,
                "description": m.description,
                "image": m.image_path,
            }
            for m in matches
        ],
    }

