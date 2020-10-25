import requests

from progrez.progrez import Progrez
from progrez.typewriter import Typewriter

# example file to download
response = requests.get('http://elementsofprogramming.com/eop.pdf', stream=True)

### SETTING UP THE BAR
bar = Progrez('$percentage$% [$paint$$progress$$erase$] Downloading data $data$ $loader$', 
              total=int(response.headers['content-length']), 
              disapear=False,
              bar_width=30)
bar.change_bar_appearance('■▪▫', left_border='', right_border='')
bar.add_painter([14, 6, 4, 7], pulse=1)
###

p = 0

for i in response.iter_content(chunk_size=4096):
    p += len(i)
    bar.update(p)
else:
    if not bar.full:
        bar.abort('requests timeout')