from app import app
import eventlet.wsgi

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 9000)), app)
