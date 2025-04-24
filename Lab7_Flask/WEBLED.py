from flask import Flask, render_template, request, jsonify
from gpiozero import PWMLED

app = Flask(__name__)
led = PWMLED(27)

@app.route('/')
def home():
    return render_template('led.html')

@app.route('/led', methods=['POST'])
def led_control():
    data = request.get_json()
    if data['action'] == 'on':
        led.on()
    elif data['action'] == 'off':
        led.off()
    elif data['action'] == 'blink':
        led.blink()
    elif data['action'] == 'brightness':
        brightness = data['brightness']
        led.value = brightness
    return jsonify({'status': 'success', 'brightness': led.value})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')