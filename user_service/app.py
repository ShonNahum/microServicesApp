from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'service': 'user_service', 'status': 'running'})

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # Mock users list
        return jsonify({'users': ['user1', 'user2']})
    elif request.method == 'POST':
        data = request.json
        return jsonify({'message': 'User added', 'user': data}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
