from flask import Flask, render_template, request, jsonify  
import requests  
from functools import wraps  
  
app = Flask(__name__)  
  
# 模拟的公开天气API接口，实际应用中需要替换为真实的API  
WEATHER_API_URL = 'https://api.example.com/weather?city={city}'  
  
def handle_exceptions(func):  
    @wraps(func)  
    def wrapper(*args, **kwargs):  
        try:  
            return func(*args, **kwargs)  
        except requests.exceptions.RequestException as e:  
            return jsonify({'error': '请求错误，请稍后再试。'}), 400  
        except Exception as e:  
            return jsonify({'error': '服务器内部错误，请稍后再试。'}), 500  
    return wrapper  
  
@app.route('/weather', methods=['GET'])  
@handle_exceptions  
def get_weather():  
    city = request.args.get('city')  
    if not city:  
        return jsonify({'error': '请输入城市名。'}), 400  
      
    response = requests.get(WEATHER_API_URL.format(city=city))  
    if response.status_code == 200:  
        weather_data = response.json()  
        return jsonify(weather_data)  
    else:  
        return jsonify({'error': '获取天气信息失败，请检查城市名是否正确。'}), 404  
  
@app.route('/')  
def index():  
    return render_template('index.html')  
  
@app.route('/search', methods=['POST'])  
def search_weather():  
    city = request.form.get('city')  
    if not city:  
        return '请输入城市名。', 400  
      
    response = requests.get(WEATHER_API_URL.format(city=city))  
    if response.status_code == 200:  
        weather_data = response.json()  
        return render_template('weather.html', weather=weather_data)  
    else:  
        return '获取天气信息失败，请检查城市名是否正确。', 404  
  
if __name__ == '__main__':  
    app.run(debug=True)