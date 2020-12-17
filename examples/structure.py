import os
import random
from time import sleep

from progrez.progrez import Progrez
from progrez.typewriter import Typewriter
from progrez.color import Color

os.system('cls' if os.name == 'nt' else 'clear')

Typewriter.write('Welcome to the Hell!', centered=1, matrix=1, bgcolor=4, fps=70, delay=1)
print()

### SETUP STARTS ###
Progrez.PAINT = 'dye' # (!) here is how you can rename keywords

bar1 = Progrez(' $percentage$% [$dye1$$progress$$erase$] Taking up some $dye2$infernal$erase$ data $speed$ $loader$', 
              total=random.randint(1200, 2000), 
              bar_width=30, 
              disapear=0, 
              blink=1)

bar2 = Progrez(' $percentage$% [$dye$$progress$$erase$] Banishing $dye1$kind$erase$ souls $loader1$', 
              total=random.randint(1200, 2000), bar_width=30, disapear=0, blink=1)
bar3 = Progrez(' $percentage$% [$dye1$$progress$$erase$] Inviting more $dye1$evils$erase$ $loader1$', 
              total=random.randint(1200, 2000), bar_width=30, disapear=0, blink=1)


bar1.change_bar_appearance('■▪▫', left_border='', right_border='') # (!) just removing the borders
bar1.add_painter(rainbow=1, done_colors=4, reverse=True)
bar1.add_painter([Color.light_cyan, Color.cyan, Color.blue, Color.light_gray], pulse=1)
bar1.add_painter(Color.red)

bar2.change_bar_appearance('■▪▫', left_border='', right_border='')
# (!) wave-like apperarance:
# bar2.change_bar_appearance("""`* •. ¸ ¸. • *' ¨` * •. ¸ ¸. • *' ¨` * •. ¸ ¸. • *' ¨` * •. ¸ ¸. • *' ¨` * •.""")
bar2.add_loader(list(reversed(['   >', '  >>', ' >>>', '>>> ', '>>  ', '>   ', '    '])))
bar2.add_painter(rainbow=1, reverse=True)
bar1.add_painter([Color.light_cyan, Color.cyan, Color.blue, Color.light_gray], pulse=1)
bar2.add_painter(Color.green)

bar3.change_bar_appearance('■▪▫', left_border='', right_border='')
bar3.add_loader(['◴', '◷', '◶', '◵'])
bar3.add_painter(Color.red)
bar3.add_painter(Color.red, done_colors=Color.blue)
### ENDS ###


### FILLING PROCESS STARTS ###
while not bar1.full:
    bar1.next(random.randint(5, 15))
    sleep(0.04)
    
while not bar2.full:
    bar2.next(random.randint(5, 15))
    sleep(0.04)
    
while not bar3.full:
    bar3.next(random.randint(5, 15))
    sleep(0.04)
### ENDS ###

print()
Typewriter.write('And you have finally become one of hellfire membership!', centered=1, matrix=1, bgcolor=4, fps=70)
