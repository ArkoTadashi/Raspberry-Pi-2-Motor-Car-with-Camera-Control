
import curses
import socket
import webbrowser


s = socket.socket()
host = '192.168.0.107'
port = 12345
s.bind((host, port))


def main(window):
    s.listen(5)

    while True:
        c, addr = s.accept()
        print('Got connection from ', addr)
        # webbrowser.open('http://' + addr[0] + ':8080')
        next_key = None
        while True:
            curses.halfdelay(1)
            if next_key is None:
                key = window.getch()
            else:
                key = next_key
                next_key = None
            if key != -1:
                # KEY PRESSED
                curses.halfdelay(3)
                print(key)
                #action = actions.get(key)
                data = 'pp smol'
                if key == 97:
                    data = 'left'
                if key == 100:
                    data = 'right'
                if key == 119:
                    data = 'forward'
                if key == 115:
                    data = 'reverse'
                # if key == 259:
                #     data = 'camfor'
                if key == 260:
                    data = 'camlef'
                # if key == 258:
                #     data = 'camrev'
                if key == 261:
                    data = 'camrig'
                # if action is not None:
                #     #action()
                #     print(action)
                c.send(data.encode())
                next_key = key
                first = False
                while next_key == key:
                    next_key = window.getch()
                    if not first:
                        next_key = key
                        first = True
                    
                # KEY RELEASED
                #stop()
                data = 'stop'
                c.send(data.encode())

curses.wrapper(main)
