from pico2d import load_image
from pico2d import get_time
#from state_machin import StateMachine
from state_machin import *

class Boy:
    def __init__(self):
        #self.name=name
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 1
        self.face_dir=0;
        self.action = 1
        #self.wait_time=0;
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {time_out:Sleep, right_down:Run ,left_down:Run ,space_down:Idle },
            Sleep:{space_down:Idle , right_down:Run ,left_down:Run},
            Run:{right_up:Idle , left_up:Idle , space_down:Run}
        })

    def update(self):
        self.state_machine.update()
        #self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT',event))
        pass

    def draw(self):
        self.state_machine.draw()

    def fire_ball(self):
        if self.action%2==0:
            print('fireball_left')
        else:
            print('fireball_right')

class Idle:
    @staticmethod
    def enter(boy,e):

        if boy.action<2:
            boy.action+=2
        #boy.dir=0
        boy.frame=0
        boy.wait_time = get_time()
        pass
        #print('Boy Idle Enter')
    @staticmethod
    def exit(boy,e):
        if space_down(e):
            boy.fire_ball()
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
        #if start_event(e):

        boy.frame=0
        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame+1)%8
    @staticmethod
    def draw(boy):
        if boy.action ==3:
            boy.image.clip_composite_draw(
                boy.frame *100, 300, 100, 100,
                3.141592/2, # 90도 회전
                '', # 좌우상하 반전 X
                boy.x - 25, boy.y - 25, 100, 100
            )
        else:
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100,
                3.141592/2*3,  # 90도 회전
                '',  # 좌우상하 반전 X
                boy.x + 25, boy.y - 25, 100, 100)

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir,boy.action=1,1
        if left_down(e) or right_up(e):
            boy.dir,boy.action=-1,0

        pass

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x+=boy.dir*5

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)