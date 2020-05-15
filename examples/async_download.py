import requests

from progrez import Progrez
from progrez import Typewriter


response = requests.get('https://www.hq.nasa.gov/alsj/a17/A17_FlightPlan.pdf', stream=True)

bar = Progrez('$percentage$% [$dye$$progress$$erase$] Taking up some infernal data $data$ with speed $speed$ $loader$', 
              total=int(response.headers['content-length']), 
              disapear=False,
              bar_width=30)
bar.change_bar_appearance('■▪▫', left_border='', right_border='')
bar.add_painter([14, 6, 4, 7], pulse=1)

p = 0

for i in response.iter_content(chunk_size=4096):
    p += len(i)
    bar.update(p)
else:
    if not bar.full:
        bar.abort('requests timeout')
        
print()
Typewriter.writeline('Completed!')