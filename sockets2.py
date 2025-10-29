'''
Bryan Kennedy
ENME441 - Lab 7 - Sockets and Network Communication

Problem 2
'''

import socket
import RPi.GPIO as GPIO

# setup GPIO pins and PWM
pins = [5, 6, 13]  # same wiring as part 1
GPIO.setmode(GPIO.BCM)
pwms = []
levels = [0, 0, 0]  # brightness for each LED

for p in pins:
    GPIO.setup(p, GPIO.OUT)
    pwm = GPIO.PWM(p, 500)  # 500 Hz
    pwm.start(0)
    pwms.append(pwm)

# helper to send normal HTTP 200 with body
def http_ok(body, ctype="text/html"):
    header = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Content-Type: {ctype}\r\n"
        "Connection: close\r\n\r\n"
    )
    return header.encode() + body

# parse POST body into dict like {"led":"1","level":"77"}
def parse_post(text):
    if "\r\n\r\n" not in text: return {}
    body = text.split("\r\n\r\n",1)[1]
    data = {}
    for part in body.split("&"):
        if "=" in part:
            k,v = part.split("=",1)
            data[k] = v
    return data

# update duty cycle for one LED
def set_led(i, value):
    i = int(i); value = int(value)
    if 0 <= i < 3 and 0 <= value <= 100:
        levels[i] = value
        pwms[i].ChangeDutyCycle(value)

# build the HTML+JS page with 3 sliders
def build_page():
    # inline JS:
    #  - when a slider moves, send POST to /set with led index + value
    #  - update the number next to that slider
    page = f"""<!doctype html>
<html>
  <body>
    <div style="border:1px solid #000;padding:15px;width:300px;font-family:sans-serif;">
      <div style="display:flex;align-items:center;margin-bottom:15px;">
        <div style="width:50px;">LED1</div>
        <input type="range" min="0" max="100" value="{levels[0]}" id="led0" style="flex:1;margin:0 10px;">
        <span id="val0">{levels[0]}</span>
      </div>

      <div style="display:flex;align-items:center;margin-bottom:15px;">
        <div style="width:50px;">LED2</div>
        <input type="range" min="0" max="100" value="{levels[1]}" id="led1" style="flex:1;margin:0 10px;">
        <span id="val1">{levels[1]}</span>
      </div>

      <div style="display:flex;align-items:center;">
        <div style="width:50px;">LED3</div>
        <input type="range" min="0" max="100" value="{levels[2]}" id="led2" style="flex:1;margin:0 10px;">
        <span id="val2">{levels[2]}</span>
      </div>
    </div>

    <script>
      // send new brightness to the Pi
      function sendUpdate(ledIndex, levelValue) {{
        // update number on screen right away
        document.getElementById("val"+ledIndex).textContent = levelValue;

        // build form body like led=1&level=77
        let body = "led=" + ledIndex + "&level=" + levelValue;

        // send POST to /set without reloading page
        fetch("/set", {{
          method: "POST",
          headers: {{
            "Content-Type": "application/x-www-form-urlencoded"
          }},
          body: body
        }});
      }}

      // hook up sliders
      function attachSlider(id, ledIndex) {{
        let slider = document.getElementById(id);
        slider.addEventListener("input", function() {{
          sendUpdate(ledIndex, slider.value);
        }});
      }}

      attachSlider("led0", 0);
      attachSlider("led1", 1);
      attachSlider("led2", 2);
    </script>
  </body>
</html>
"""
    return page.encode()

# minimal HTTP router:
# GET  /      -> send page
# POST /set   -> update LED brightness, return "OK"
# anything else -> 404
def handle_request(req_text):
    # first line looks like "GET / HTTP/1.1"
    first_line = req_text.split("\r\n")[0]
    parts = first_line.split(" ")
    if len(parts) < 2:
        return http_ok(b"bad request","text/plain")

    method = parts[0]
    path = parts[1]

    if method == "GET" and path == "/":
        return http_ok(build_page(), "text/html")

    if method == "POST" and path == "/set":
        data = parse_post(req_text)
        led = data.get("led","0")
        level = data.get("level","0")
        set_led(led, level)
        return http_ok(b"OK","text/plain")

    # fallback 404
    body = b"404 not found"
    header = (
        "HTTP/1.1 404 Not Found\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n\r\n"
    )
    return header.encode() + body

# open socket and serve requests
s = socket.socket()
s.bind(("",8080))
s.listen(1)
print("Server ready on http://bkpi.local:8080  (Problem 2)")

try:
    while True:
        c,a = s.accept()
        req = c.recv(2048).decode()  # read browser request (a little bigger buffer now)
        resp = handle_request(req)   # decide what to do
        c.sendall(resp)              # send HTTP response
        c.close()

except KeyboardInterrupt:
    pass
finally:
    for p in pwms: p.stop()
    GPIO.cleanup()
    s.close()
