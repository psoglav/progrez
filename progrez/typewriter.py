import shutil
import platform
from time import sleep

import term
from progrez.progrez import Progrez

WIN = platform.system() == 'Windows'

if WIN:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    from pynput.keyboard import Key, Listener

class Typewriter(object):
    __current_char_index = 0
    __entity = ''
    __stop = False
    goals = []
    framerate = Progrez._Framerate(15)

    @classmethod
    def add_to_queue(cls, goals, indent=0, centered=False):
        w = shutil.get_terminal_size()[0]

        if isinstance(goals, list):
            for goal in goals:
                if centered:
                    cls.goals.append(goal.center(w, ' '))
                else:
                    cls.goals.append((' ' * indent) + goal)
        else:
            if centered:
                    cls.goals.append(goals.center(w, ' '))
            else:
                cls.goals.append((' ' * indent) + goals)

    @classmethod
    def write(cls, msg='', indent=0, fgcolor=7, bgcolor=0, fps=None, matrix=False, centered=False, delay=0):
        cls.add_to_queue(msg if msg else '', indent=indent, centered=centered)
        cls.perform_goals(fgcolor, bgcolor, fps=fps, matrix=matrix, delay=delay)

    @classmethod
    def writeline(cls, msg='', indent=0, fgcolor=7, bgcolor=0, fps=None, centered=False, delay=0):
        cls.add_to_queue(msg if msg else '', indent=indent, centered=centered)
        cls.perform_goals(fgcolor, bgcolor, newline=True, fps=fps, delay=delay)

    @classmethod
    def rewrite(cls, msg='', indent=0, fgcolor=7, bgcolor=0, fps=None, matrix=False, centered=False, delay=0):
        cls.add_to_queue(msg if msg else '', indent=indent, centered=centered)
        cls.perform_goals(fgcolor, bgcolor, rewrite=not matrix, fps=fps, matrix=matrix, delay=delay)

    @classmethod
    def rewriteline(cls, msg='', indent=0, fgcolor=7, bgcolor=0, fps=None, centered=False, delay=0):
        cls.add_to_queue(msg if msg else '', indent=indent, centered=centered)
        cls.perform_goals(fgcolor, bgcolor, newline=True, rewrite=True, fps=fps, delay=delay)

    @classmethod
    def perform_goals(cls, fgcolor=7, bgcolor=0,
                      rewrite=False, newline=False,
                      fps=None, delay=0,
                      centered=False, matrix=False):
        if not cls.goals:
            Exception("Current launching doesn't make sense. There are no more goals.")

        if isinstance(fps, int) and fps >= 0: Typewriter.framerate.add_temp(fps)
        else: Typewriter.framerate.del_temp()

        if rewrite and not matrix:
            term.writeLine()
            term.up()
            term.clearLine()

        if WIN:
            listener = Listener(on_press=cls.__on_pressed)
            listener.start()

        while not cls.__done(matrix, delay, newline):
            if cls.framerate.next or cls.__stop or not fps:
                if matrix:
                    print(f'\033[3{fgcolor}m' + f'\033[4{bgcolor}m' + cls.__next(1)[1], end='\r')
                else:
                    term.write(f'\033[3{fgcolor}m' + f'\033[4{bgcolor}m' + cls.__next()[0])
        else:
            if matrix and not rewrite:
                print('\033[37m\033[40m')
            else:
                if newline:
                    term.writeLine('\033[37m\033[40m')
                else:
                    term.write('\033[37m\033[40m')

        if WIN: listener.stop()


    @classmethod
    def __done(cls, matrix=0, delay=0, newline=0):
        if not cls.goals:
            return 1
        else:
            if not matrix:
                if cls.goals[0] == cls.__entity:
                    del cls.goals[0]
                    cls.__entity = ''
                    cls.__current_char_index = 0
                    cls.__stop = False
                    sleep(delay)
            else:
                if cls.goals[0] == ''.join(cls.Matrix._entity):
                    del cls.goals[0]
                    cls.__entity = ''
                    cls.__current_char_index = 0
                    cls.Matrix._reset()
                    cls.__stop = False

                    if newline and cls.goals:
                        print()

                    sleep(delay)

            if not cls.goals:
                return 1
            else:
                return 0

    @classmethod
    def __next(cls, matrix=0):
        char = cls.goals[0][-1]

        if not matrix:
            if cls.__current_char_index < len(cls.goals[0]):
                char = cls.goals[0][cls.__current_char_index]
                cls.__entity += char
                cls.__current_char_index += 1

            return (char, cls.__entity)
        else:
            if cls.__current_char_index < len(cls.goals[0]):
                char = cls.goals[0][cls.__current_char_index]
                cls.Matrix._add_to_track(char)
                cls.__current_char_index += 1

            return (char, cls.Matrix._translated())

    @classmethod
    def __on_pressed(cls, key):
        if key == Key.esc:
            cls.__stop = True

    class Matrix:
        _entity = []
        __tracked = []
        __characters = '.WwlEzYPL-U/0x2Qc6$%IO=ZVvbe91JH^!~r@tXC?;qa4NsdBM&#:fy"g3FDhj*uiop5R+7kTnKGSAm8'
        framerate = Progrez._Framerate(120)

        @classmethod
        def _translated(cls):
            if cls.framerate.next:
                for i, e in enumerate(cls._entity):
                    track = cls.__tracked[i]

                    if track != -1:
                        char_index = cls.__characters.find(e) + 1

                        if char_index == len(cls.__characters) - 1:
                            char_index = track

                        cls._entity[i] = cls.__characters[char_index]

                        if cls.__characters.find(cls._entity[i]) == track:
                            cls.__tracked[i] = -1

            return ''.join(cls._entity)

        @classmethod
        def _add_to_track(cls, char):
            cls._entity.append(char[0])
            cls.__tracked.append(cls.__characters.find(char))

        @classmethod
        def _reset(cls):
            cls._entity = []
            cls.__tracked = []
