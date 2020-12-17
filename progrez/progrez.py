import sys
import time
import signal
import threading
from time import sleep
from shutil import get_terminal_size

import re
import term
import colored


class Progrez(threading.Thread):
    PAINT = 'paint'
    ERASE = 'erase'
    LOADER = 'loader'
    PROGRESS = 'progress'
    PERCENTAGE = 'percentage'
    DATA = 'data'
    SPEED = 'speed'

    class _Framerate:
        def __init__(self, per_second=10):
            self.next_timepoint = 0
            self.per_second = per_second
            self.__previous_fps = per_second

        @property
        def per_second(self):
            return self.__per_second

        @per_second.setter
        def per_second(self, fps):
            self.__per_second = fps
            self.__previous_fps = fps

        def add_temp(self, fps):
            """
            Adding a temporary framerate for single execution.
            """
            self.__per_second = fps

        def del_temp(self):
            """
            Deleting the temporary framerate for single execution.
            """
            self.__per_second = self.__previous_fps

        @property
        def next(self):
            t = time.time()

            if t >= self.next_timepoint and self.per_second:
                self.next_timepoint = t + 1 / self.per_second
                return 1
            elif self.per_second == 0:
                return 1
            else:
                return 0

    class __Loader(_Framerate):
        def __init__(self, frames=['    ', '   <', '  <<', ' <<<', '<<< ', '<<  ', '<   ']):
            Progrez._Framerate.__init__(self, 15)
            self.frames = frames

        def entity(self):
            if self.frames:
                if self.next:
                    self.frames.append(self.frames.pop(0))

                return self.frames[0]
            else:
                return 'NO_FRAMES'

    class __Painter(_Framerate):
        def __init__(self, colors, done_colors, index, rainbow, pulse, reverse):
            self.index = index

            if not colors:  # colors by default
                if rainbow:
                    self.colors = [13, 9, 11, 10, 14, 12]
                elif pulse:
                    self.colors = [15, 14, 15, 15, 15, 14,
                                   15, 15, 14, 15, 14, 14, 14, 14, 15]
                else:
                    self.colors = [1]
            else:
                self.colors = colors

            Progrez._Framerate.__init__(self, 15)
            self.marvelous = (0, 1 if rainbow else 2)[pulse ^ rainbow]
            self.fluid_colors = []
            self.reverse = reverse
            self.done_colors = done_colors

        def entity(self, s, last_update):
            kw = f'\\${Progrez.PAINT}{self.index if self.index else "0?"}\\$'

            def split():
                start = re.split(kw, s, 1)
                end = [el for el in re.split(
                    f'(\\${Progrez.PAINT}\\d*\\$)|(\\${Progrez.ERASE}\\$)', start[1], 1) if isinstance(el, str)]

                return [start[0], end[0], *end[1::]]

            ss = split()

            def merge(painted):
                return ''.join([ss[0], painted, *ss[2::]])

            def shift():
                if not self.reverse:
                    self.fluid_colors = [
                        self.fluid_colors.pop(-1)] + self.fluid_colors
                else:
                    self.fluid_colors = self.fluid_colors + \
                        [self.fluid_colors.pop(0)]

            def rainbow():
                if not self.fluid_colors:
                    rc = self.colors.copy()
                    cc = rc.copy()
                    length = len(ss[1])
                    res = []

                    while length > 0:
                        if len(cc) == 1:
                            rc = list(reversed(rc))
                            cc = rc.copy()

                        res.append(cc.pop(0))
                        length -= 1

                    self.fluid_colors = res
                else:
                    shift()

                return self.fluid_colors

            def pulse():
                length = len(ss[1])

                if not self.fluid_colors:
                    cc = self.colors.copy()
                    self.fluid_colors = [
                        cc[-1] for i in range(length)] + [cc.pop(0) for _ in range(len(cc) - 1)]
                else:
                    shift()

                return self.fluid_colors[:length:]

            def paint(colors):
                cc = colors.copy()
                prepared = list(ss[1])
                painted = ''

                for char in prepared:
                    painted += colored.fg(cc.pop(0) if len(cc)
                                          > 1 else cc[0]) + char

                painted += colored.fg(7)

                return merge(painted)

            if self.colors:
                if last_update:
                    return paint(self.done_colors)

                if self.marvelous == 1:
                    if self.next:
                        rainbow()

                    return paint(self.fluid_colors)
                elif self.marvelous == 2:
                    if self.next:
                        pulse()

                    return paint(self.fluid_colors)
                else:
                    return paint(self.colors)

            return s

    def __init__(self, structure, bar_width=15, total=100, disapear=True, blink=False, data_unit=''):
        threading.Thread.__init__(self)
        signal.signal(signal.SIGINT, self.__cancel_handler)

        self.name = str(self)
        self.__exit_flag = 0

        # appearance
        self.rebuild_structure(structure)
        self.__data_unit = data_unit
        self.__loaders = [Progrez.__Loader()]
        self.__painters = []
        self.__blink = blink
        self.__disapear = disapear
        self.__bar_width = bar_width
        self.__bar_appearance = {
            'left_border': '[',
            'right_border': ']',
            'inside': '■▪▫'
        }

        # progress
        self.total = total
        self.__current = 0
        self.__download_speed = []
        self.__ads = 0
        self.__ads_frequency = Progrez._Framerate(
            1)  # for average download speed

        # switch
        self.__entity_update = True
        self.__first_update = True
        self.__last_update = False
        self.__up_stream = False

        # text
        self.__previous_entity = ''
        self.__error = ''

    @property
    def __keywords(self):
        items = {}

        items[Progrez.PROGRESS] = self.__progress
        items[Progrez.DATA] = self.__data
        items[Progrez.PERCENTAGE] = self.percentage
        items[Progrez.LOADER] = self.__loader
        items[Progrez.PAINT] = self.__painter
        items[Progrez.SPEED] = self.download_speed

        return items

    def update(self, value=0):
        if not self.__up_stream:
            self.start()

        self.__previus_progress = self.__current
        self.__current = (self.total, value)[value <= self.total]
        self.__download_speed.append(
            self.__current - self.__previus_progress)  # doesnt work properly

        if self.full:
            self.stop()

    def next(self, value=1):
        self.update(self.__current + value)

    def rebuild_structure(self, new):
        self.__structure = list(
            filter(None, re.split(r'(\$[a-z0-9]+\$)', new)))

    def add_loader(self, frames):
        self.__loaders += [Progrez.__Loader(frames)]

    def add_painter(self, colors=[], done_colors=[7], rainbow=False, pulse=False, reverse=False):
        colors = colors if not isinstance(colors, int) else [colors]
        done_colors = done_colors if not isinstance(
            done_colors, int) else [done_colors]

        self.__painters += [Progrez.__Painter(
            colors, done_colors, len(self.__painters), rainbow, pulse, reverse)]

    def change_bar_appearance(self, inside, **kwargs):
        if 'left_border' in kwargs:
            self.__bar_appearance = {'left_border': ''}
        if 'right_border' in kwargs:
            self.__bar_appearance = {'right_border': ''}

        kwargs.update({'inside': inside})
        self.__bar_appearance.update(kwargs)

    def __progress(self):
        b = self.__bar_appearance
        bw = self.__bar_width

        fill = b['inside'][0] * bw
        caret = b['inside'][1:len(b['inside'])-1:]
        empty = b['inside'][len(b['inside'])-1] * bw

        inside = fill + caret + empty
        p = self.percentage(bw + len(caret))

        return b['left_border'] + inside[bw+len(caret)-p: bw*2+len(caret)-p] + b['right_border']

    def __data(self):
        current = self.__format_data(
            self.__current, use_unit=False, regarding_the=self.total)
        total = self.__format_data(self.total)

        return (f'{current}/' if not self.full else '') + f'{total}'

    def __format_data(self, value, use_unit=True, regarding_the=0):
        unit = self.__data_unit

        if not unit:
            reagarding = regarding_the if regarding_the else value

            if reagarding > 999999:
                unit = 'mb'
            elif reagarding > 999:
                unit = 'kb'
            else:
                unit = 'b'

        if unit == 'kb':
            return f'{round(value / 1000, 2)}kb' if use_unit else f'{round(value / 1000, 2)}'
        elif unit == 'mb':
            return f'{round(value / 1_000_000, 2)}mb' if use_unit else f'{round(value / 1_000_000, 2)}'

    def download_speed(self):
        if self.__ads_frequency.next and self.__download_speed:
            self.__ads = sum(
                self.__download_speed) // len(self.__download_speed)
            self.__download_speed = []

        speed = self.__format_data(self.__ads)

        return speed + '/s' if speed else ''

    def percentage(self, entire=100):
        p = int(self.__current / self.total * entire)
        return p if p < entire else entire

    def __loader(self, index=0):
        if index < len(self.__loaders):
            return self.__loaders[index]
        else:
            return 0

    def __painter(self, index=0):
        if index < len(self.__painters):
            return self.__painters[index]
        else:
            return 0

    def __entity(self):
        e = ''
        painters = []

        for s in self.__structure:  # translation
            keyword = self.__is_keyword(s)

            if keyword:
                if keyword in [Progrez.LOADER, Progrez.PAINT, Progrez.ERASE]:
                    if self.__last_update and keyword == Progrez.LOADER:  # removing loader when progrez is finished
                        continue
                    elif keyword == Progrez.ERASE:
                        e += s
                        continue

                    index = re.findall(r'\d+', s)
                    answer = self.__keywords[keyword](
                        int(index[0])) if index else self.__keywords[keyword]()

                    if not answer:
                        self.__error = f"You don't have any {keyword} number {index[0]}."
                    elif isinstance(answer, Progrez.__Loader):
                        e += answer.entity()
                    elif isinstance(answer, Progrez.__Painter):
                        painters.append(answer)
                        e += s

                elif keyword in self.__keywords:
                    # index = re.findall(r'\d+', s)
                    answer = self.__keywords[keyword]()
                    e += str(answer)

                else:
                    self.__error = f'There is no {s} keyword.'
            else:
                e += s

        e = self.__paint(e, painters)

        if self.__previous_entity != e:  # to avoid extra updates
            self.__previous_entity = e
            self.__entity_update = True

        # return error if we've reached this point
        return (e, self.__error)[bool(self.__error)]

    def __is_keyword(self, s):
        if s[0] == '$' and s[-1] == '$':
            return s.strip('$1234567890')
        else:
            return ''

    def __paint(self, s, painters):
        for painter in painters:
            s = painter.entity(s, self.__last_update)

        return re.sub(f'\\${Progrez.ERASE}\\$', '', s)

    def run(self):
        self.__up_stream = 1
        self.async_flush()

    def async_flush(self):
        while not self.__exit_flag:
            self.__flush()
            sleep(0.001)

    def __flush(self, entity=''):
        if entity:
            self.__print(entity)
            return

        e = self.__entity()

        if self.__entity_update and e:
            self.__print(e)
            self.__entity_update = False

    @staticmethod
    def escape_ansi(s):
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

        return ansi_escape.sub('', s)

    def __print(self, s):  # prints the bar
        if self.__first_update:
            term.down()

        if not self.__last_update or not self.__blink:
            delta = ((get_terminal_size()[0] - len(Progrez.escape_ansi(s))) * ' ')
            print('\033[A' + s + delta)

        else:
            term.up()
            term.clearLine()
            colors = re.findall(r'\[38;5;(\d+)m', s)
            store_colors = []  # without duplicates

            for c in colors:
                if c not in store_colors:
                    store_colors.append(c)

            for i in range(6):
                clear = i % 2 == 0
                ss = s

                if clear:
                    for c in store_colors:
                        ss = re.sub(f'\\[38;5;{c}m', '[38;5;0m', ss)

                term.writeLine(ss, term.black if clear else term.white)
                term.up()
                sleep(0.06)
            
        self.__first_update = False

    def __finish(self):
        if self.__disapear:
            term.clearLine()
        else:
            term.down()

    @property
    def full(self):
        return self.__current >= self.total

    def __cancel_handler(self, signal, frame):
        self.abort()
        sys.exit(0)

    def abort(self, msg='cancelled by the user'):
        self.stop()
        self.__blink = False
        self.__flush(f'Progress bar is aborted: {msg}.')
        self.__finish()

    def stop(self):
        self.__exit_flag = 1
        self.__last_update = True
        self.__flush()
        self.__finish()
