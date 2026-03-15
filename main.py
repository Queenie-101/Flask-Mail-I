from flask import Flask, render_template, request, session
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "mysecretkey123"

# Gmail details
EMAIL_ADDRESS = "queenestheradekanmi@gmail.com"
EMAIL_PASSWORD = "ttjc ytku qxxj hvf"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/verify", methods=["POST"])
def verify():
    email = request.form["email"]

    # generate random OTP
    otp = random.randint(100000, 999999)

    # store email and otp
    session["email"] = email
    session["otp"] = str(otp)

    # create email message
    subject = "Your OTP Code"
    body = f"Hello,\n\nYour OTP is: {otp}\n\nUse it to verify your account."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    try:
        # connect to gmail server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        return render_template("verification.html")

    except Exception as e:
        return f"Error sending email: {e}"


@app.route("/validate", methods=["POST"])
def validate():
    user_otp = request.form["otp"]
    saved_otp = session.get("otp")

    if user_otp == saved_otp:
        return """
        <html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <h2 class="success">OTP Verified Successfully ✅</h2>
                <a href="/">Go Back</a>
            </div>
        </body>
        </html>
        """
    else:
        return """
        <html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <h2 class="error">Invalid OTP ❌</h2>
                <a href="/">Try Again</a>
            </div>
        </body>
        </html>
        """


if __name__ == "__main__":
    app.run(debug=True)