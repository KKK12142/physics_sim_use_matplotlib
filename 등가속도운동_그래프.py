import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider

class Simulation:
    def __init__(self):
        self.s_0 = 0
        self.v_0 = 0
        self.a = 9.8
        self.t = np.linspace(0, 10, 100)
        self.s = self.v_0*self.t + 0.5*self.a*self.t**2
        self.v = self.v_0 + self.a*self.t
        self.a_arr = np.full_like(self.t, self.a)  # a 배열 (그래프용)

    def calculate(self):
        self.s = self.s_0 + self.v_0 * self.t + 0.5 * self.a * self.t ** 2
        self.v = self.v_0 + self.a * self.t
        self.a_arr = np.full_like(self.t, self.a)  # a는 스칼라 유지, 배열은 따로
        return self.s, self.v, self.a_arr

    def update(self, v_0=None, a=None, s_0=None):
        if v_0 is not None:
            self.v_0 = v_0
        if a is not None:
            self.a = a
        if s_0 is not None:
            self.s_0 = s_0
        return self.calculate()

sim = Simulation()

def setup_axis(ax):
    # 위, 오른쪽 테두리 숨기기
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 왼쪽, 아래 축을 원점으로 이동
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    # 축 끝에 화살표 추가
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    # x >= 0 영역만
    ax.set_xlim(0, None)

fig, ax = plt.subplots(1, 3, figsize=(12, 6))
plt.subplots_adjust(bottom=0.45)
line_s, = ax[0].plot(sim.t, sim.s)
line_v, = ax[1].plot(sim.t, sim.v)
line_a, = ax[2].plot(sim.t, sim.a_arr)

for a in ax:
    setup_axis(a)

ax[0].set_title('Position vs Time')
ax[0].set_xlabel('t (s)', loc='right')
ax[0].set_ylabel('s (m)', loc='top')

ax[1].set_title('Velocity vs Time')
ax[1].set_xlabel('t (s)', loc='right')
ax[1].set_ylabel('v (m/s)', loc='top')

ax[2].set_title('Acceleration vs Time')
ax[2].set_xlabel('t (s)', loc='right')
ax[2].set_ylabel('a (m/s^2)', loc='top')

ax_s0 = plt.axes([0.15, 0.3, 0.65, 0.03])
s0_slider = Slider(ax_s0, '$s_0$', -200, 200, valinit=sim.s_0)

ax_v0 = plt.axes([0.15, 0.1, 0.65, 0.03])
v0_slider = Slider(ax_v0, '$v_0$', -20, 20, valinit=sim.v_0)

ax_a0 = plt.axes([0.15, 0.2, 0.65, 0.03])
a0_slider = Slider(ax_a0, '$a$', -10, 10, valinit=sim.a)


def on_change(val):
    s, v, a = sim.update(v_0=v0_slider.val, a=a0_slider.val, s_0=s0_slider.val)
    line_s.set_ydata(s)
    line_v.set_ydata(v)
    line_a.set_ydata(a)
    ax[0].autoscale_view()
    fig.canvas.draw_idle()

v0_slider.on_changed(on_change)
a0_slider.on_changed(on_change)
s0_slider.on_changed(on_change)

# 리셋 버튼
ax_reset = plt.axes([0.8, 0.02, 0.1, 0.04])
btn_reset = Button(ax_reset, 'Reset')

def reset(event):
    v0_slider.reset()
    a0_slider.reset()
    s0_slider.reset()

btn_reset.on_clicked(reset)

plt.show()