from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import resend
import os

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- RESEND ----------------
resend.api_key = "re_KfocVB3h_HT5s2WGHBCi6oi3DEodG4HD9"  # 🔴 change after deploy (use env later)

# ---------------- DATABASE ----------------
DATABASE_URL = "sqlite:///./form.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class FormData(Base):
    __tablename__ = "form_data"

    id = Column(Integer, primary_key=True, index=True)
    first = Column(String, nullable=True)
    last = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    source = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# ---------------- WEBSITE EMAIL MAP ----------------
WEBSITE_EMAIL_MAP = {
    "dhruvfabrotech.in": "archanagaikwadpro@gmail.com",
    "shivkrupatensile.com": "alpana.pawar@dwipl.co.in"
}

# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "Backend Working ✅"}


@app.post("/submit")
def submit_form(
    first: str = Form(None),
    last: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None),
    message: str = Form(None),
    source: str = Form(None)
):
    try:
        # ✅ Handle empty fields
        first = first or ""
        last = last or ""
        email = email or ""
        phone = phone or ""
        message = message or ""
        source = source or "unknown"

        # ✅ Get dynamic email
        receiver_email = WEBSITE_EMAIL_MAP.get(source, "alpana.pawar@dwipl.co.in")

        # ✅ Save to DB
        db = SessionLocal()
        new_entry = FormData(
            first=first,
            last=last,
            email=email,
            phone=phone,
            message=message,
            source=source
        )
        db.add(new_entry)
        db.commit()
        db.close()

        # ✅ Send email
        resend.Emails.send({
            "from": "noreply@dwipl.co.in",  # 🔥 after domain verify
            "to": [receiver_email],
            "cc": ["alpanakakde@gmail.com"],

            "reply_to": email,
            "subject": "New Contact Form",

            "html": f"""
                <h3>New Contact Form</h3>

                <table border="1" cellpadding="8" style="border-collapse: collapse;">
                <tr><td><b>Source</b></td><td>{source}</td></tr>
                <tr><td><b>Name</b></td><td>{first} {last}</td></tr>
                <tr><td><b>Email</b></td><td>{email}</td></tr>
                <tr><td><b>Phone</b></td><td>{phone}</td></tr>
                <tr><td><b>Message</b></td><td>{message}</td></tr>
                </table>
            """
        })

        return {"message": "Email sent & saved ✅"}

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}