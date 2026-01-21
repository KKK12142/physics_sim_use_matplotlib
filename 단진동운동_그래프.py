"""
토크(돌림힘) 시각화: τ = r × F
Physics STEM Visualizer 스킬 기반 - 라이트 모드
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import numpy as np

# 한글 폰트 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_prop = fm.FontProperties(fname=font_path)

# 색상 팔레트 (라이트 테마)
COLORS = {
    'background': '#ffffff',
    'force': '#16a34a',      # 힘 벡터 - 녹색
    'torque': '#9333ea',     # 토크 - 보라색
    'pivot': '#ea580c',      # 회전축 - 주황색
    'r_vector': '#2563eb',   # 위치벡터 - 파란색
    'highlight': '#ca8a04',  # 강조 - 노란색/금색
    'text': '#1f2937',       # 텍스트 - 어두운 회색
    'lever': '#9ca3af',      # 지렛대
    'box_bg': '#f3f4f6',     # 박스 배경
    'box_border': '#d1d5db', # 박스 테두리
}

fig, ax = plt.subplots(1, 1, figsize=(12, 9), facecolor=COLORS['background'])
ax.set_facecolor(COLORS['background'])

# 축 설정
ax.set_xlim(-1, 8)
ax.set_ylim(-2, 7)
ax.set_aspect('equal')
ax.axis('off')

# === 회전축 (Pivot Point) ===
pivot = np.array([1.5, 2])
pivot_circle = plt.Circle(pivot, 0.15, color=COLORS['pivot'], zorder=10)
ax.add_patch(pivot_circle)
ax.plot(pivot[0], pivot[1], 'o', color='white', markersize=5, zorder=11)

# 회전축 라벨
ax.text(pivot[0], pivot[1] - 0.5, '회전축 O', fontproperties=font_prop, 
        fontsize=12, color=COLORS['pivot'], ha='center', va='top', fontweight='bold')

# === 지렛대 (Lever Arm) ===
lever_end = np.array([6, 2])
ax.plot([pivot[0], lever_end[0]], [pivot[1], lever_end[1]], 
        color=COLORS['lever'], linewidth=8, solid_capstyle='round', zorder=1)

# === 위치 벡터 r ===
r_end = np.array([5.5, 2])
ax.annotate('', xy=r_end, xytext=pivot,
            arrowprops=dict(arrowstyle='->', color=COLORS['r_vector'], 
                          lw=3, mutation_scale=20))
# r 라벨
r_mid = (pivot + r_end) / 2
ax.text(r_mid[0], r_mid[1] - 0.4, r'$\vec{r}$', fontsize=20, 
        color=COLORS['r_vector'], ha='center', va='top', fontweight='bold')

# === 힘 벡터 F ===
F_start = r_end
F_direction = np.array([0.7, 1])  # 대각선 방향
F_direction = F_direction / np.linalg.norm(F_direction)  # 정규화
F_magnitude = 2.5
F_end = F_start + F_direction * F_magnitude

ax.annotate('', xy=F_end, xytext=F_start,
            arrowprops=dict(arrowstyle='->', color=COLORS['force'], 
                          lw=4, mutation_scale=25))
# F 라벨
F_label_pos = F_start + F_direction * F_magnitude * 0.6 + np.array([0.3, 0])
ax.text(F_label_pos[0], F_label_pos[1], r'$\vec{F}$', fontsize=20, 
        color=COLORS['force'], ha='left', va='center', fontweight='bold')

# === 각도 θ 표시 ===
r_direction = (r_end - pivot) / np.linalg.norm(r_end - pivot)
theta = np.arccos(np.dot(r_direction, F_direction))

# 각도 호 그리기
angle_radius = 0.8
angle_start = 0  # r 벡터 방향 (수평)
angle_end = np.degrees(np.arctan2(F_direction[1], F_direction[0]))

arc = patches.Arc(F_start, angle_radius*2, angle_radius*2, 
                  angle=0, theta1=angle_start, theta2=angle_end,
                  color=COLORS['highlight'], lw=2, linestyle='--')
ax.add_patch(arc)

# θ 라벨
theta_label_angle = np.radians((angle_start + angle_end) / 2)
theta_label_pos = F_start + np.array([np.cos(theta_label_angle), 
                                       np.sin(theta_label_angle)]) * (angle_radius + 0.3)
ax.text(theta_label_pos[0], theta_label_pos[1], r'$\theta$', fontsize=18, 
        color=COLORS['highlight'], ha='center', va='center', fontweight='bold')

# === 토크 방향 (페이지 밖으로 나오는 방향) ===
torque_pos = pivot + np.array([0, 1.2])
# 원 안에 점 (페이지 밖으로 나오는 방향 표시)
torque_circle = plt.Circle(torque_pos, 0.25, fill=False, 
                           color=COLORS['torque'], lw=3, zorder=10)
ax.add_patch(torque_circle)
ax.plot(torque_pos[0], torque_pos[1], 'o', color=COLORS['torque'], 
        markersize=8, zorder=11)

# 토크 라벨
ax.text(torque_pos[0] + 0.5, torque_pos[1], r'$\vec{\tau}$', fontsize=20, 
        color=COLORS['torque'], ha='left', va='center', fontweight='bold')
ax.text(torque_pos[0], torque_pos[1] + 0.5, '(지면 밖으로)', fontproperties=font_prop,
        fontsize=10, color=COLORS['torque'], ha='center', va='bottom')

# === 회전 방향 표시 (반시계 방향) ===
rotation_arc = patches.FancyArrowPatch(
    pivot + np.array([0.8, 0.6]), 
    pivot + np.array([0.8, -0.6]),
    connectionstyle="arc3,rad=0.5",
    arrowstyle='->', color=COLORS['torque'], lw=2, 
    mutation_scale=15, alpha=0.7
)
ax.add_patch(rotation_arc)

# === 수식 박스 ===
formula_box = patches.FancyBboxPatch((0, 4.5), 7.5, 2.2, 
                                      boxstyle="round,pad=0.1,rounding_size=0.2",
                                      facecolor=COLORS['box_bg'], 
                                      edgecolor=COLORS['torque'],
                                      linewidth=2)
ax.add_patch(formula_box)

# 공식 텍스트
ax.text(3.75, 6.2, '돌림힘 (토크)', fontproperties=font_prop, fontsize=18, 
        color=COLORS['text'], ha='center', va='center', fontweight='bold')

ax.text(3.75, 5.5, r'$\vec{\tau} = \vec{r} \times \vec{F}$', fontsize=26, 
        color=COLORS['text'], ha='center', va='center')

ax.text(3.75, 4.85, r'$|\tau| = r \cdot F \cdot \sin\theta$', fontsize=18, 
        color=COLORS['highlight'], ha='center', va='center', fontweight='bold')

# === 범례 박스 ===
legend_box = patches.FancyBboxPatch((5.5, -1.5), 2.3, 1.8,
                                     boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor=COLORS['box_bg'], 
                                     edgecolor=COLORS['box_border'],
                                     linewidth=1.5)
ax.add_patch(legend_box)

# 범례 항목
legend_items = [
    (COLORS['r_vector'], r'$\vec{r}$', '위치 벡터'),
    (COLORS['force'], r'$\vec{F}$', '힘 벡터'),
    (COLORS['torque'], r'$\vec{\tau}$', '토크'),
]

for i, (color, symbol, label) in enumerate(legend_items):
    y_pos = -0.0 - i * 0.5
    ax.plot([5.7], [y_pos], 's', color=color, markersize=10)
    ax.text(6.1, y_pos, symbol, fontsize=14, color=color, ha='left', va='center')
    ax.text(6.5, y_pos, label, fontproperties=font_prop, fontsize=11, 
            color=COLORS['text'], ha='left', va='center')

# === 힘 작용점 표시 ===
ax.plot(F_start[0], F_start[1], 'o', color=COLORS['highlight'], 
        markersize=10, zorder=9)
ax.text(F_start[0] + 0.3, F_start[1] - 0.3, '작용점', fontproperties=font_prop,
        fontsize=10, color=COLORS['highlight'], ha='left', va='top', fontweight='bold')

# === 팔 길이 표시 ===
ax.annotate('', xy=(pivot[0], F_start[1] + F_magnitude * F_direction[1] * 0.4), 
            xytext=(pivot[0], pivot[1]),
            arrowprops=dict(arrowstyle='<->', color='#6b7280', 
                          lw=1.5, linestyle='--'))

# 하단 설명
ax.text(3.75, -1.8, '오른손 법칙: 손가락을 r→F 방향으로 감으면 엄지가 τ 방향', 
        fontproperties=font_prop, fontsize=11, color='#6b7280', 
        ha='center', va='center', style='italic')

# plt.savefig('/home/claude/torque_diagram_light.png', dpi=150, 
#             facecolor=COLORS['background'], edgecolor='none',
#             bbox_inches='tight', pad_inches=0.3)
plt.show()

print("토크 다이어그램 생성 완료: torque_diagram_light.png")
