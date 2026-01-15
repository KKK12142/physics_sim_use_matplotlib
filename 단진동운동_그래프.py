import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from matplotlib.animation import FuncAnimation

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

class Simulation:
    def __init__(self):
        self.t = np.linspace(0, 10, 1000)
        self.v_0 = 0 #[m/s]
        self.A = 0.5 #[m]
        self.k = 100 #[N/m]
        self.m = 1 #[kg]
        self.phi = 0 #[rad]
        self.omega = np.sqrt(self.k/self.m)
        self.calculate()

    def calculate(self):
        self.x = self.A * np.cos(self.omega * self.t + self.phi)
        self.v = -1 * self.A * self.omega * np.sin(self.omega * self.t + self.phi)
        self.a = -1 * self.A * self.omega**2 * np.cos(self.omega * self.t + self.phi)

    def update(self, m=None, k=None, A=None):
        if m is not None:
            self.m = m
        if k is not None:
            self.k = k
        if A is not None:
           self.A = A
        self.omega = np.sqrt(self.k/self.m)
        return self.calculate()

sim = Simulation()

# 그래프 설정
fig, ax = plt.subplots(1, 3, figsize=(14, 6))
plt.subplots_adjust(bottom=0.35, top=0.85, wspace=0.3)

# 메인 제목
fig.suptitle('단순조화운동 (Simple Harmonic Motion)', fontsize=14, fontweight='bold')

# 각 서브플롯 설정
titles = ['변위 (Displacement)', '속도 (Velocity)', '가속도 (Acceleration)']
ylabels = ['x [m]', 'v [m/s]', 'a [m/s²]']
colors = ['blue', 'green', 'red']
labels = ['x = A·cos(ωt + φ)', 'v = -Aω·sin(ωt + φ)', 'a = -Aω²·cos(ωt + φ)']

lines = []
for i in range(3):
    ax[i].set_title(titles[i], fontsize=11)
    ax[i].set_xlabel('시간 t [s]', fontsize=10)
    ax[i].set_ylabel(ylabels[i], fontsize=10)
    ax[i].set_xlim(0, 10)
    ax[i].grid(True, alpha=0.3)
    line, = ax[i].plot([], [], color=colors[i], label=labels[i], linewidth=1.5)
    ax[i].legend(loc='upper right', fontsize=8)
    lines.append(line)

# y축 범위 설정
def set_ylim():
    ax[0].set_ylim(-sim.A * 1.2, sim.A * 1.2)
    ax[1].set_ylim(-sim.A * sim.omega * 1.2, sim.A * sim.omega * 1.2)
    ax[2].set_ylim(-sim.A * sim.omega**2 * 1.2, sim.A * sim.omega**2 * 1.2)

set_ylim()

# 슬라이더 설정
ax_m = plt.axes([0.25, 0.18, 0.5, 0.03])
ax_k = plt.axes([0.25, 0.12, 0.5, 0.03])
ax_A = plt.axes([0.25, 0.06, 0.5, 0.03])

m_slider = Slider(ax_m, '질량 m [kg]', 0.1, 10, valinit=1)
k_slider = Slider(ax_k, '탄성계수 k [N/m]', 1, 200, valinit=100)
A_slider = Slider(ax_A, '진폭 A [m]', 0.1, 1, valinit=0.5)

# 애니메이션 상태 변수
animation_state = {'frame_idx': 0, 'is_playing': True}

# 애니메이션 초기화 함수
def init():
    for line in lines:
        line.set_data([], [])
    return lines

# 애니메이션 업데이트 함수
def animate(frame):
    if animation_state['is_playing']:
        animation_state['frame_idx'] = frame

    idx = animation_state['frame_idx']
    t_data = sim.t[:idx]
    lines[0].set_data(t_data, sim.x[:idx])
    lines[1].set_data(t_data, sim.v[:idx])
    lines[2].set_data(t_data, sim.a[:idx])
    return lines

# 슬라이더 변경 시 호출
def on_change(val):
    sim.update(m=m_slider.val, k=k_slider.val, A=A_slider.val)
    set_ylim()
    animation_state['frame_idx'] = 0

m_slider.on_changed(on_change)
k_slider.on_changed(on_change)
A_slider.on_changed(on_change)

# 재생/일시정지 버튼
ax_play = plt.axes([0.4, 0.01, 0.08, 0.03])
ax_reset = plt.axes([0.52, 0.01, 0.08, 0.03])

btn_play = Button(ax_play, '일시정지')
btn_reset = Button(ax_reset, '재시작')

def toggle_play(event):
    animation_state['is_playing'] = not animation_state['is_playing']
    btn_play.label.set_text('재생' if not animation_state['is_playing'] else '일시정지')

def reset_animation(event):
    animation_state['frame_idx'] = 0

btn_play.on_clicked(toggle_play)
btn_reset.on_clicked(reset_animation)

# 애니메이션 생성
ani = FuncAnimation(fig, animate, init_func=init, frames=len(sim.t),
                    interval=20, blit=True, repeat=True)

plt.show()
