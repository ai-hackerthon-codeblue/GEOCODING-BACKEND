import socketio

# 표준 파이썬 클라이언트
sio = socketio.Client()

# 테스트용 샘플 경로 데이터
sample_path = [
    {'lat': 37.5665, 'lng': 126.9780},
    {'lat': 37.5666, 'lng': 126.9781},
    {'lat': 37.5667, 'lng': 126.9782},
    {'lat': 37.5668, 'lng': 126.9783},
    {'lat': 37.5669, 'lng': 126.9784},
]

@sio.event
def connect():
    print('서버에 연결되었습니다.')
    print('시뮬레이션을 시작합니다...')
    sio.emit('start_simulation', {'path': sample_path})

@sio.event
def connect_error(data):
    print('서버 연결에 실패했습니다!')

@sio.event
def disconnect():
    print('서버와 연결이 끊어졌습니다.')

@sio.on('location_update')
def on_location_update(data):
    print(f"위치 업데이트 수신 ({data['step']}/{data['total_steps']}): {data['point']}")

@sio.on('simulation_end')
def on_simulation_end(data):
    print(f"시뮬레이션 종료: {data['message']}")
    sio.disconnect()

if __name__ == '__main__':
    try:
        sio.connect('http://localhost:5000')
        sio.wait()
    except Exception as e:
        print(f"오류 발생: {e}")
