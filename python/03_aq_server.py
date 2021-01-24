from bottle import route, run, template
from aq import AQ

aq = AQ()

page = """
<h1>Raspberry Pi Air Quality Meter</h1>
<table>
  <tr><th>Temp (C)</th><th>{{t}}</th></tr>
  <tr><th>eCO2 (ppm)</th><th>{{c}}</th></tr>
</table>
"""

@route('/')
def index():
    temp_c = str(aq.get_temp())
    eco2 = str(aq.get_eco2())
    return template(page, t=temp_c, c=eco2)

run(host='0.0.0.0', port=8080)
