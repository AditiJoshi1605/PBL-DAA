from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Mock API: Return route info (not complete)
@app.route('/api/routes', methods=['GET'])
def get_routes():
    return jsonify([
        {"data  variables"},
        {"data variables"}
    ])

if __name__ == '__main__':
    socketio.run(app, debug=True)
