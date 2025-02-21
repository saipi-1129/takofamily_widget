from flask import Flask, jsonify
import requests
import datetime
import pytz

# タイムゾーンを東京に設定
tokyo_tz = pytz.timezone('Asia/Tokyo')

app = Flask(__name__)

# 配信状況を取得する関数
def get_is_live():
    url = "https://www.mirrativ.com/api/catalog/follow"
    headers = {
        "x-os-push": "1",
        "x-uuid": "",
        "HTTP_X_TIMEZONE": "Asia/Tokyo",
        "x-referer": "home.follow",
        "Accept": "*/*",
        "Accept-Language": "ja",
        "Accept-Encoding": "gzip, deflate, br",
        "x-unity-framework": "5.13.0",
        "x-adjust-adid": "",
        "x-adjust-idfa": "",
        "User-Agent": "MR_APP/10.85.0/iOS/iPhone14,7/18.0.1",
        "x-client-unixtime": "1740123361.054889",
        "x-ad": "",
        "x-idfv": "",
        "x-network-status": "2",
        "Connection": "keep-alive",
        "Cookie": "
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()
    
    # 配信中かどうかをリストから取得
    is_live_count = 0
    for item in response_json.get("list", []):
        live = item.get("live")
        if live and live.get("is_live"):
            is_live_count += 1

    return is_live_count

@app.route('/is_live')
def is_live():
    now = datetime.datetime.now(tokyo_tz)
    today = now.strftime('%Y-%m-%d')
    try:
        live_status_count = get_is_live()
    except Exception as e:
        return jsonify({'status': 'error', 'time': f'{today} {now.strftime("%H:%M:%S")}', 'message': f'データ取得に失敗しました: {str(e)}'})
    
    return jsonify({'status': 'ok', 'time': f'{today} {now.strftime("%H:%M:%S")}', 'message': '現在配信中の人数', 'is_live': live_status_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
