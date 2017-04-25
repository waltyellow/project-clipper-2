from app import server as server
from app import main

if __name__ == '__main__':
    print('Spinning up the server')
    server.run(debug=True)
