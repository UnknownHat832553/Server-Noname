from flask import Flask, redirect, request, session, url_for, render_template
import requests

app = Flask(__name__)
app.secret_key = 'SERVERNONAME8353'
client_id = '1338841311478022164'
client_secret = '8msNjww1Syei_qbgzVFYvlt_VAp4W2GR'
redirect_uri = 'https://unknownhat832553.github.io/Server-NoName/'  # เปลี่ยน URL ให้เป็น Localhost ตอนพัฒนา
webhook_url = "https://discordapp.com/api/webhooks/1338100822734536766/2E_STl59I0kATK7_-uOSZfRa5DooCkUTU39-tGmSR8Lv35WNDROM3kE0Np2JTBicyVOu"

@app.route('/')
def index():
    return render_template('index.html')  # ใช้ index.html เป็นหน้าแรก

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
    session['user'] = user_data

    # ส่งข้อมูลไป Webhook
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

    # เปลี่ยนเส้นทางไปหน้า home.html
    return redirect(url_for('home_page'))

@app.route('/home')
def home_page():
    if 'user' in session:
        user = session['user']
        return render_template('home.html', user=user)
    return redirect(url_for('login'))  # ถ้ายังไม่ได้ล็อกอินให้กลับไปล็อกอินก่อน

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
