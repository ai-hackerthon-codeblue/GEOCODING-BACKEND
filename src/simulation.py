import time
from flask_socketio import SocketIO, emit

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    """클라이언트 연결 시 호출됩니다."""
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """클라이언트 연결 해제 시 호출됩니다."""
    print('Client disconnected')

@socketio.on('start_simulation')
def handle_start_simulation(data):
    """
    'start_simulation' 이벤트를 수신하면 경로 시뮬레이션을 시작합니다.
    data 에는 'path' 키로 좌표 리스트가 포함되어야 합니다.
    """
    path = data.get('path')
    if not path or not isinstance(path, list):
        emit('simulation_error', {'error': 'Invalid path data'})
        return

    print(f"Starting simulation for path with {len(path)} points.")

    for i, point in enumerate(path):
        emit('location_update', {
            'point': point,
            'step': i + 1,
            'total_steps': len(path)
        })
        print(f"Sent point {i+1}/{len(path)}: {point}")
        socketio.sleep(1)

    emit('simulation_end', {'message': 'Simulation completed'})
    print("Simulation ended.")
