from pico2d import load_image
from pico2d import get_time
#from state_machin import StateMachine
from state_machin import *

class Boy:
    def __init__(self):
        #self.name=name
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        #self.wait_time=0;
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {time_out:Sleep},
            Sleep:{space_down:Idle}})

    def update(self):
        self.state_machine.update()
        #self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT',event))
        pass

    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)

class Idle:
    @staticmethod
    def enter(boy,e):
        boy.action=3
        boy.dir=0
        boy.frame=0
        boy.wait_time = get_time()
        pass
        #print('Boy Idle Enter')
    @staticmethod
    def exit(boy,e):
        #print('Boy Idle Exit')
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame+1)%8
        if get_time() - boy.wait_time>2:
            boy.state_machine.add_event(('TIME_OUT',0))
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy,e):
        #boy.frame=0
        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame+1)%8
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(
            boy.frame *100, 300, 100, 100,
            3.141592/2, # 90도 회전
            '', # 좌우상하 반전 X
            boy.x - 25, boy.y - 25, 100, 100
        )
