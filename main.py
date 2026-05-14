from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import resend
import os

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- RESEND API KEY ----------------
# resend.api_key = os.getenv("re_KfocVB3h_HT5s2WGHBCi6oi3DEodG4HD9")
resend.api_key = "re_KfocVB3h_HT5s2WGHBCi6oi3DEodG4HD9"


@app.get("/")
def home():
    return {"message": "Backend Working ✅"}


@app.post("/submit")
def submit_form(
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    source: str = Form(...) 
):
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": ["alpana.pawar@dwipl.co.in"],  # test mode
            
            "reply_to": email,
            "subject": "Test Contact Form",
            "html": f"""
    <h2>New Contact Form Submission</h2>

    <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: Arial;">
        
        <tr>
            <th align="left">Field</th>
            <th align="left">Value</th>
        </tr>

        <tr>
            <td><b>Source</b></td>
            <td>{source}</td>
        </tr>

        <tr>
            <td><b>Name</b></td>
            <td>{name}</td>
        </tr>

        <tr>
            <td><b>Phone</b></td>
            <td>{phone}</td>
        </tr>

        <tr>
            <td><b>Email</b></td>
            <td>{email}</td>
        </tr>

        <tr>
            <td><b>Message</b></td>
            <td>{message}</td>
        </tr>

    </table>

    <br>
    <p style="color: gray; font-size: 12px;">
        This email was sent from your website contact form.
    </p>
"""
        })

        return {"message": "Email sent successfully ✅"}

    except Exception as e:
        print("Error:", e)  # helps debugging
        return {"error": str(e)}