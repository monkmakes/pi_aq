from bottle import route, run, template
from aq import AQ

aq = AQ()

page = """
<b>Temp (C) {{t}} eCO2 (ppm) {{c}}</b>
"""

@route('/')
def index():
    temp_c = str(aq.get_temp())
    eco2 = str(aq.get_eco2())
    return template(page, t=temp_c, c=eco2)

run(host='0.0.0.0', port=8080)
