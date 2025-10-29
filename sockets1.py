'''
Bryan Kennedy
ENME441 - Lab 7 - Sockets and Network Communication

Problem 1
'''

import socket
import RPi.GPIO as GPIO

# setup GPIO pins and PWM
pins = [5, 6, 13]
GPIO.setmode(GPIO.BCM)
pwms = []
levels = [0, 0, 0]  # store brightness for each LED

for p in pins:
    GPIO.setup(p, GPIO.OUT)
    pwm = GPIO.PWM(p, 500)  # 500 Hz PWM
    pwm.start(0)
    pwms.append(pwm)
    
# create HTML page for browser
def htmlPage(selected = 0):
    html = f"""<!doctype html>
    <html><body>
    <h2>Raspberry Pi (bkpi) LED Brightness</h2>
    <form method="POST" action="/">
    <p>Brightness:
     <input type="range" name="level" min="0" max="100" value="{levels[selected]}">
     </p>
     <p>Select LED:<br>
     <input type="radio" name="led" value="0" {"checked" if selected==0 else ""}>LED 1 ({levels[0]}%)<br>
     <input type="radio" name="led" value="1" {"checked" if selected==1 else ""}>LED 2 ({levels[1]}%)<br>
     <input type="radio" name="led" value="2" {"checked" if selected==2 else ""}>LED 3 ({levels[2]}%)<br>
  </p>
  <p><input type="submit" value="Change Brightness"></p>
  </form>
  </body></html>"""
    return html.encode()  # return HTML as bytes

# build HTTP 200 OK response
def ok(body):
    header = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Content-Type: text/html\r\n"
        "Connection: close\r\n\r\n"
    )
    return header.encode() + body

# read POST data sent from the form
def parse_post(text):
    if "\r\n\r\n" not in text: return {}
    body = text.split("\r\n\r\n",1)[1]
    data = {}
    for part in body.split("&"):
        if "=" in part:
            k,v = part.split("=",1)
            data[k] = v
    return data

# update LED brightness using PWM
def set_led(i, value):
    i = int(i); value = int(value)
    if 0 <= i < 3 and 0 <= value <= 100:
        levels[i] = value
        pwms[i].ChangeDutyCycle(value)

# start basic socket web server
s = socket.socket()
s.bind(("",8080))
s.listen(1)
print("Server ready on http://bkpi.local:8080")

try:
    while True:
        c,a = s.accept()  # wait for browser connection
        req = c.recv(1024).decode()
        method = req.split(" ")[0]  # check GET or POST

        if method == "POST":
            d = parse_post(req)  # extract form data
            led = d.get("led","0")
            level = d.get("level","0")
            set_led(led, level)  # update PWM
            c.sendall(ok(htmlPage(int(led))))  # send updated page
        else:
            c.sendall(ok(htmlPage()))  # show default page
        c.close()

except KeyboardInterrupt:
    pass
finally:
    for p in pwms: p.stop()
    GPIO.cleanup()
    s.close()
