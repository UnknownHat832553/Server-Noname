from flask import Flask, redirect, request, session
import requests

app = Flask(__name__)
app.secret_key = 'SERVERNONAME8353'
client_id = '1338841311478022164'
client_secret = '8msNjww1Syei_qbgzVFYvlt_VAp4W2GR'
redirect_uri = 'https://unknownhat832553.github.io/Server-NoName/'
webhook_url = "https://discordapp.com/api/webhooks/1338100822734536766/2E_STl59I0kATK7_-uOSZfRa5DooCkUTU39-tGmSR8Lv35WNDROM3kE0Np2JTBicyVOu"

@app.route('/')
def home():
    return '<a href="/login">ล็อกอินด้วย Discord</a>'

@app.route('/login')
def login():
    discord_oauth_url = f'https://discord.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify'
    return redirect(discord_oauth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    access_token = response.json().get('access_token')
    
    user_info = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': f'Bearer {access_token}'})
    user_data = user_info.json()

    webhook_data = {
        "content": f"✅ **{user_data['username']}** (ID: {user_data['id']}) ได้ทำการล็อกอินเข้าเว็บแล้ว!",
        "embeds": [
            {
                "title": "User Info",
                "color": 5763719,
                "fields": [
                    {"name": "Username", "value": user_data['username'], "inline": True},
                    {"name": "User ID", "value": user_data['id'], "inline": True}
                ],
                "thumbnail": {"url": f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png"}
            }
        ]
    }
    requests.post(webhook_url, json=webhook_data)

    return f"Hello, {user_data['username']}!"

if __name__ == '__main__':
    app.run(debug=True)
