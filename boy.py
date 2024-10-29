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
        self.size =100;
        #self.wait_time=0;
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions({
            Idle: {time_out:Sleep, right_down:Run ,left_down:Run ,space_down:Idle,a_down:Auto_Run },
            Sleep:{space_down:Idle , right_down:Run ,left_down:Run ,a_down:Auto_Run},
            Run:{right_up:Idle , left_up:Idle , space_down:Run,a_down:Auto_Run},
            Auto_Run: {time_out:Idle }
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
        if boy.dir==1:
            if boy.x<800:
                boy.x+=boy.dir*5
        else:
            if boy.x>0:
                boy.x+=boy.dir*5


    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Auto_Run:
    @staticmethod
    def enter(boy, e):
        if boy.action%2==1:
            boy.dir, boy.action = 1, 1
        else:
            boy.dir, boy.action = -1, 0
        boy.wait_time = get_time()
        boy.size =200
        pass

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()
        boy.size = 100
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 15
        if boy.x>800:
            boy.dir,boy.action=-1,0
        elif boy.x<0:
            boy.dir, boy.action = 1, 1

        # if get_time() - boy.wait_time < 2.5:
        # #if boy.size <200:
        #     boy.size += 1
        # else:
        #     boy.size -= 1

        if get_time() - boy.wait_time>5:
            boy.state_machine.add_event(('TIME_OUT',0))

    @staticmethod
    def draw(boy):
        size =boy.size
        #boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100,100, boy.x, boy.y)
        boy.image.clip_composite_draw( boy.frame * 100, boy.action * 100, 100, 100,
            0,  # 90도 회전
            '',  # 좌우상하 반전 X
            boy.x , boy.y +size//5, size,size)
