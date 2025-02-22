import os
import requests
from flask import Flask, redirect, request, session, jsonify
from dotenv import load_dotenv

# โหลดตัวแปรจาก .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ตั้งค่า OAuth2
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
DISCORD_API_URL = "https://discord.com/api"
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route("/")
def login():
    auth_url = (
        f"{DISCORD_API_URL}/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}" 
        f"&response_type=code&scope=identify"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: No code provided", 400
    
    # ขอ Token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{DISCORD_API_URL}/oauth2/token", data=data, headers=headers)
    token_data = response.json()
    token = token_data.get("access_token")
    if not token:
        return "Error: Failed to get access token", 400

    # ขอข้อมูลผู้ใช้
    headers = {"Authorization": f"Bearer {token}"}
    user_data = requests.get(f"{DISCORD_API_URL}/users/@me", headers=headers).json()
    
    # ส่งข้อมูลไปยังเซิร์ฟเวอร์ Discord
    send_to_discord(user_data)
    
    return jsonify(user_data)

# ฟังก์ชันส่งข้อมูลไปยังเซิร์ฟเวอร์ Discord ผ่าน Webhook
def send_to_discord(user):
    if not WEBHOOK_URL:
        print("Error: Webhook URL is not set")
        return
    payload = {
        "content": f"👤 ผู้ใช้ล็อกอิน: {user['username']}#{user['discriminator']} (ID: {user['id']})"
    }
    requests.post(WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    app.run(debug=True)