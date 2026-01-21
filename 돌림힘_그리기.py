import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Arc, FancyBboxPatch, Circle, Wedge
import numpy as np
import streamlit as st
# 스타일 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'dejavusans'

# 색상 팔레트
BLUE = '#2563eb'
RED = '#dc2626'
GREEN = '#16a34a'
ORANGE = '#ea580c'
PURPLE = '#7c3aed'
GRAY = '#6b7280'
BROWN = '#92400e'
CYAN = '#0891b2'

def draw_arrow(ax, start, end, color, label='', label_offset=(0.3, 0), fontsize=14, lw=3):
    """화살표와 라벨을 그리는 함수"""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))
    if label:
        mid = ((start[0]+end[0])/2 + label_offset[0], 
               (start[1]+end[1])/2 + label_offset[1])
        ax.text(mid[0], mid[1], label, fontsize=fontsize, color=color, 
                fontweight='bold', ha='center', va='center')

def setup_clean_ax(ax, xlim, ylim):
    """깔끔한 축 설정"""
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_visible(False)
    # ax.set_xticks([])
    # ax.set_yticks([])

# ============================================
# 1. 돌림힘 기본 개념 다이어그램
# ============================================
fig1, ax1 = plt.subplots(figsize=(10, 8))
setup_clean_ax(ax1, (-2, 10), (-2, 8))

# 회전축 (피벗 포인트)
pivot = (1, 3)
ax1.plot(*pivot, 'ko', markersize=20, zorder=5)
ax1.plot(*pivot, 'wo', markersize=12, zorder=6)
ax1.text(pivot[0], pivot[1]-0.8, 'Pivot\n(Axis)', fontsize=12, ha='center', va='top', color=GRAY)

# 막대 (레버)
rod_end = (8, 3)
ax1.plot([pivot[0], rod_end[0]], [pivot[1], rod_end[1]], color=BROWN, lw=8, solid_capstyle='round')

# 거리 벡터 r
r_end = (7, 3)
draw_arrow(ax1, pivot, r_end, BLUE, r'$\vec{r}$', (0, -0.6), fontsize=18, lw=3)

# 힘 벡터 F (수직으로 작용)
F_start = r_end
F_end = (7, 6)
draw_arrow(ax1, F_start, F_end, RED, r'$\vec{F}$', (0.5, 0), fontsize=18, lw=4)

# 회전 방향 표시
rotation_arc = Arc(pivot, 3, 3, angle=0, theta1=0, theta2=60, color=GREEN, lw=3)
ax1.add_patch(rotation_arc)
ax1.annotate('', xy=(2.2, 4.5), xytext=(2.5, 4.2),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=2))
ax1.text(3.2, 5, r'$\tau$', fontsize=20, color=GREEN, fontweight='bold')

# 수식
ax1.text(5, 7.2, r'$\vec{\tau} = \vec{r} \times \vec{F}$', fontsize=24, 
         ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.9))

# 거리 표시
ax1.annotate('', xy=(7, 2.3), xytext=(1, 2.3),
            arrowprops=dict(arrowstyle='<->', color=GRAY, lw=1.5))
ax1.text(4, 1.8, r'$r$ (moment arm)', fontsize=14, ha='center', color=GRAY)

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/torque_01_basic.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("torque_01_basic.png 생성 완료")

# ============================================
# 2. 모멘트 팔 - 각도에 따른 변화
# ============================================
fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(14, 6))

# 왼쪽: 수직으로 힘 작용 (θ = 90°)
setup_clean_ax(ax2a, (-1, 8), (-1, 7))
ax2a.set_title(r'$\theta = 90°$ (Maximum Torque)', fontsize=16, fontweight='bold', pad=10)

pivot_a = (1, 2)
ax2a.plot(*pivot_a, 'ko', markersize=15)
ax2a.plot([pivot_a[0], 6], [pivot_a[1], 2], color=BROWN, lw=6, solid_capstyle='round')

# r 벡터
draw_arrow(ax2a, pivot_a, (5.5, 2), BLUE, r'$\vec{r}$', (0, -0.5), fontsize=16, lw=2.5)

# F 벡터 (수직)
draw_arrow(ax2a, (5.5, 2), (5.5, 5.5), RED, r'$\vec{F}$', (0.5, 0), fontsize=16, lw=3)

# 직각 표시
rect = patches.Rectangle((5.1, 2), 0.4, 0.4, fill=False, edgecolor=ORANGE, lw=2)
ax2a.add_patch(rect)

ax2a.text(4, 5.5, r'$\tau = rF\sin(90°) = rF$', fontsize=14, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

# 오른쪽: 비스듬히 힘 작용 (θ = 45°)
setup_clean_ax(ax2b, (-1, 8), (-1, 7))
ax2b.set_title(r'$\theta = 45°$ (Reduced Torque)', fontsize=16, fontweight='bold', pad=10)

pivot_b = (1, 2)
ax2b.plot(*pivot_b, 'ko', markersize=15)
ax2b.plot([pivot_b[0], 6], [pivot_b[1], 2], color=BROWN, lw=6, solid_capstyle='round')

# r 벡터
draw_arrow(ax2b, pivot_b, (5.5, 2), BLUE, r'$\vec{r}$', (0, -0.5), fontsize=16, lw=2.5)

# F 벡터 (45도 기울어짐)
theta = np.radians(45)
F_len = 3.5
F_end_b = (5.5 + F_len*np.cos(theta), 2 + F_len*np.sin(theta))
draw_arrow(ax2b, (5.5, 2), F_end_b, RED, r'$\vec{F}$', (0.5, 0.3), fontsize=16, lw=3)

# F의 수직 성분 (점선)
F_perp = F_len * np.sin(theta)
ax2b.plot([5.5, 5.5], [2, 2 + F_perp], '--', color=PURPLE, lw=2)
ax2b.text(5.9, 2 + F_perp/2, r'$F\sin\theta$', fontsize=12, color=PURPLE)

# 각도 표시
angle_arc = Arc((5.5, 2), 1.5, 1.5, angle=0, theta1=90, theta2=135, color=ORANGE, lw=2)
ax2b.add_patch(angle_arc)
ax2b.text(5.1, 3.2, r'$\theta$', fontsize=14, color=ORANGE)

ax2b.text(4, 5.5, r'$\tau = rF\sin(45°) = \frac{rF}{\sqrt{2}}$', fontsize=14, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/torque_02_moment_arm.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("torque_02_moment_arm.png 생성 완료")

# ============================================
# 3. 각도에 따른 돌림힘 그래프
# ============================================
fig3, ax3 = plt.subplots(figsize=(10, 6))

theta_vals = np.linspace(0, 180, 100)
tau_vals = np.sin(np.radians(theta_vals))

ax3.plot(theta_vals, tau_vals, color=BLUE, lw=3, label=r'$\tau = rF\sin\theta$')
ax3.fill_between(theta_vals, tau_vals, alpha=0.2, color=BLUE)

# 특정 점 표시
ax3.plot(90, 1, 'ro', markersize=12, zorder=5)
ax3.annotate(r'Maximum at $\theta=90°$', xy=(90, 1), xytext=(110, 0.85),
            fontsize=12, arrowprops=dict(arrowstyle='->', color=RED))

ax3.plot(0, 0, 'go', markersize=10, zorder=5)
ax3.plot(180, 0, 'go', markersize=10, zorder=5)
ax3.text(10, 0.1, r'$\theta=0°$', fontsize=11, color=GREEN)
ax3.text(165, 0.1, r'$\theta=180°$', fontsize=11, color=GREEN)

ax3.set_xlabel(r'$\theta$ (degrees)', fontsize=14)
ax3.set_ylabel(r'$\tau / (rF)$', fontsize=14)
ax3.set_title('Torque vs Angle', fontsize=16, fontweight='bold')
ax3.set_xlim(0, 180)
ax3.set_ylim(0, 1.2)
ax3.grid(True, alpha=0.3)
ax3.set_xticks([0, 30, 60, 90, 120, 150, 180])

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/torque_03_graph.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("torque_03_graph.png 생성 완료")

# ============================================
# 4. 스패너(렌치) 비교
# ============================================
fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(14, 6))

# 왼쪽: 짧은 스패너
setup_clean_ax(ax4a, (-2, 8), (-2, 6))
ax4a.set_title('Short Wrench', fontsize=16, fontweight='bold', pad=10)

# 볼트 (회전축)
bolt_a = Circle((0, 2), 0.4, facecolor='gray', edgecolor='black', lw=2)
ax4a.add_patch(bolt_a)
ax4a.text(0, 2, '+', fontsize=16, ha='center', va='center', fontweight='bold')

# 짧은 스패너
wrench_a = FancyBboxPatch((0.3, 1.7), 3, 0.6, boxstyle="round,pad=0.05",
                           facecolor='silver', edgecolor='black', lw=2)
ax4a.add_patch(wrench_a)

# 힘과 거리
draw_arrow(ax4a, (3, 2), (3, 4.5), RED, r'$\vec{F}$', (0.5, 0), fontsize=16, lw=3)
ax4a.annotate('', xy=(3, 1.2), xytext=(0, 1.2),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=2))
ax4a.text(1.5, 0.7, r'$r_1$', fontsize=16, color=BLUE, ha='center')

ax4a.text(3, 5.2, r'$\tau_1 = r_1 F$', fontsize=16, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# 오른쪽: 긴 스패너
setup_clean_ax(ax4b, (-2, 10), (-2, 6))
ax4b.set_title('Long Wrench', fontsize=16, fontweight='bold', pad=10)

# 볼트
bolt_b = Circle((0, 2), 0.4, facecolor='gray', edgecolor='black', lw=2)
ax4b.add_patch(bolt_b)
ax4b.text(0, 2, '+', fontsize=16, ha='center', va='center', fontweight='bold')

# 긴 스패너
wrench_b = FancyBboxPatch((0.3, 1.7), 6, 0.6, boxstyle="round,pad=0.05",
                           facecolor='silver', edgecolor='black', lw=2)
ax4b.add_patch(wrench_b)

# 힘과 거리
draw_arrow(ax4b, (6, 2), (6, 4.5), RED, r'$\vec{F}$', (0.5, 0), fontsize=16, lw=3)
ax4b.annotate('', xy=(6, 1.2), xytext=(0, 1.2),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=2))
ax4b.text(3, 0.7, r'$r_2$', fontsize=16, color=BLUE, ha='center')

ax4b.text(5, 5.2, r'$\tau_2 = r_2 F$', fontsize=16, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# 비교 설명
ax4b.text(5, -1.2, r'$r_2 > r_1 \Rightarrow \tau_2 > \tau_1$', fontsize=18, ha='center',
         color=GREEN, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/torque_04_wrench.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("torque_04_wrench.png 생성 완료")

# ============================================
# 5. 시소 균형 (돌림힘 평형)
# ============================================
fig5, ax5 = plt.subplots(figsize=(12, 7))
setup_clean_ax(ax5, (-7, 7), (-3, 6))
ax5.set_title('Torque Equilibrium (Seesaw)', fontsize=18, fontweight='bold', pad=10)

# 받침점 (삼각형)
pivot = [(0, 0), (-0.5, -1), (0.5, -1)]
triangle = patches.Polygon(pivot, facecolor='gray', edgecolor='black', lw=2)
ax5.add_patch(triangle)

# 시소 판
ax5.plot([-5.5, 5.5], [0, 0], color=BROWN, lw=10, solid_capstyle='round')

# 왼쪽 물체 (m1)
box1 = FancyBboxPatch((-5, 0.1), 1.2, 1.2, boxstyle="round,pad=0.05",
                       facecolor='lightblue', edgecolor='black', lw=2)
ax5.add_patch(box1)
ax5.text(-4.4, 0.7, r'$m_1$', fontsize=14, ha='center', va='center')

# 오른쪽 물체 (m2)
box2 = FancyBboxPatch((2.8, 0.1), 1.2, 1.2, boxstyle="round,pad=0.05",
                       facecolor='lightcoral', edgecolor='black', lw=2)
ax5.add_patch(box2)
ax5.text(3.4, 0.7, r'$m_2$', fontsize=14, ha='center', va='center')

# 왼쪽 힘 (중력)
draw_arrow(ax5, (-4.4, 0), (-4.4, -2), BLUE, r'$m_1 g$', (-0.7, 0), fontsize=14, lw=3)

# 오른쪽 힘 (중력)
draw_arrow(ax5, (3.4, 0), (3.4, -2), RED, r'$m_2 g$', (0.7, 0), fontsize=14, lw=3)

# 거리 표시
ax5.annotate('', xy=(-4.4, -2.5), xytext=(0, -2.5),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.5))
ax5.text(-2.2, -2.9, r'$r_1$', fontsize=14, color=BLUE, ha='center')

ax5.annotate('', xy=(3.4, -2.5), xytext=(0, -2.5),
            arrowprops=dict(arrowstyle='<->', color=RED, lw=1.5))
ax5.text(1.7, -2.9, r'$r_2$', fontsize=14, color=RED, ha='center')

# 회전 방향 표시
# 반시계 (왼쪽 힘으로 인한)
arc1 = Arc((0, 0), 2, 2, angle=0, theta1=120, theta2=180, color=BLUE, lw=2, linestyle='--')
ax5.add_patch(arc1)
ax5.text(-1.5, 1.2, r'$\tau_1$', fontsize=12, color=BLUE)

# 시계 (오른쪽 힘으로 인한)
arc2 = Arc((0, 0), 2, 2, angle=0, theta1=0, theta2=60, color=RED, lw=2, linestyle='--')
ax5.add_patch(arc2)
ax5.text(1.3, 1.2, r'$\tau_2$', fontsize=12, color=RED)

# 평형 조건
ax5.text(0, 4.5, 'Equilibrium Condition:', fontsize=14, ha='center', fontweight='bold')
ax5.text(0, 3.5, r'$\sum \tau = 0$', fontsize=20, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
ax5.text(0, 2.2, r'$m_1 g r_1 = m_2 g r_2$', fontsize=16, ha='center', color=GREEN)

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/torque_05_seesaw.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("torque_05_seesaw.png 생성 완료")

# ============================================
# 6. 오른손 법칙 다이어그램
# ============================================
fig6, ax6 = plt.subplots(figsize=(10, 8))
setup_clean_ax(ax6, (-3, 7), (-2, 8))
ax6.set_title('Right-Hand Rule for Torque', fontsize=18, fontweight='bold', pad=10)

# 회전축
pivot6 = (2, 3)
ax6.plot(*pivot6, 'ko', markersize=15)

# r 벡터 (x 방향)
draw_arrow(ax6, pivot6, (5, 3), BLUE, r'$\vec{r}$', (0, -0.5), fontsize=18, lw=3)

# F 벡터 (y 방향)
draw_arrow(ax6, (5, 3), (5, 6), RED, r'$\vec{F}$', (0.5, 0), fontsize=18, lw=3)

# 토크 벡터 (z 방향, 종이에서 나오는)
ax6.plot(5, 3, 'o', markersize=30, markerfacecolor='white', markeredgecolor=GREEN, markeredgewidth=3)
ax6.plot(5, 3, '.', markersize=15, color=GREEN)  # 점 (나오는 방향)
ax6.text(5.8, 3, r'$\vec{\tau}$', fontsize=18, color=GREEN, fontweight='bold', va='center')
ax6.text(5, 2.2, '(out of page)', fontsize=11, color=GREEN, ha='center')

# 회전 방향 표시
rotation_arc = Arc(pivot6, 4, 4, angle=0, theta1=0, theta2=70, color=ORANGE, lw=3)
ax6.add_patch(rotation_arc)
ax6.annotate('', xy=(3.8, 5), xytext=(4.2, 4.6),
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2))

# 좌표축
ax6.annotate('', xy=(0, 0), xytext=(-1, 0),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
ax6.annotate('', xy=(0, 1), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
ax6.text(-1.3, 0, 'x', fontsize=12, color=GRAY, va='center')
ax6.text(0, 1.3, 'y', fontsize=12, color=GRAY, ha='center')
ax6.plot(0, 0, 'o', markersize=15, markerfacecolor='white', markeredgecolor=GRAY, markeredgewidth=1.5)
ax6.plot(0, 0, '.', markersize=8, color=GRAY)
ax6.text(0.3, -0.3, 'z', fontsize=12, color=GRAY)

# 설명 박스
explanation = (
    "1. Point fingers along $\\vec{r}$\n"
    "2. Curl fingers toward $\\vec{F}$\n"
    "3. Thumb points in $\\vec{\\tau}$ direction"
)
ax6.text(0, 6.5, explanation, fontsize=13, va='top',
         bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

# 부호 규약
ax6.text(0, -1, 'CCW (out of page): $\\tau > 0$', fontsize=12, color=GREEN)
ax6.text(4, -1, 'CW (into page): $\\tau < 0$', fontsize=12, color=PURPLE)

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/torque_06_righthand.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("torque_06_righthand.png 생성 완료")

# ============================================
# 7. 문 열기 비교 다이어그램
# ============================================
fig7, (ax7a, ax7b) = plt.subplots(1, 2, figsize=(14, 7))

# 왼쪽: 손잡이 부분 밀기 (효율적)
setup_clean_ax(ax7a, (-1, 10), (-1, 8))
ax7a.set_title('Push at Handle (Easy)', fontsize=16, fontweight='bold', pad=10, color=GREEN)

# 경첩 (회전축)
hinge_a = Circle((0, 4), 0.3, facecolor='darkgray', edgecolor='black', lw=2)
ax7a.add_patch(hinge_a)
ax7a.text(0, 4, '+', fontsize=14, ha='center', va='center', color='white', fontweight='bold')

# 문
door_a = FancyBboxPatch((0.2, 0.5), 8, 7, boxstyle="round,pad=0.02",
                         facecolor='#d4a574', edgecolor='#8B4513', lw=3)
ax7a.add_patch(door_a)

# 손잡이
handle_a = Circle((7, 4), 0.25, facecolor='gold', edgecolor='black', lw=2)
ax7a.add_patch(handle_a)

# 힘 벡터
draw_arrow(ax7a, (7, 4), (7, 7), RED, r'$\vec{F}$', (0.5, 0), fontsize=16, lw=3)

# 거리 표시
ax7a.annotate('', xy=(7, 0.2), xytext=(0, 0.2),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=2))
ax7a.text(3.5, -0.3, r'$r$ (large)', fontsize=14, color=BLUE, ha='center')

ax7a.text(5, -0.9, r'$\tau = rF$ (Large torque!)', fontsize=14, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# 오른쪽: 경첩 근처 밀기 (비효율적)
setup_clean_ax(ax7b, (-1, 10), (-1, 8))
ax7b.set_title('Push Near Hinge (Hard)', fontsize=16, fontweight='bold', pad=10, color=RED)

# 경첩
hinge_b = Circle((0, 4), 0.3, facecolor='darkgray', edgecolor='black', lw=2)
ax7b.add_patch(hinge_b)
ax7b.text(0, 4, '+', fontsize=14, ha='center', va='center', color='white', fontweight='bold')

# 문
door_b = FancyBboxPatch((0.2, 0.5), 8, 7, boxstyle="round,pad=0.02",
                         facecolor='#d4a574', edgecolor='#8B4513', lw=3)
ax7b.add_patch(door_b)

# 손잡이 (힘 작용점 근처)
handle_b = Circle((7, 4), 0.25, facecolor='gold', edgecolor='black', lw=2)
ax7b.add_patch(handle_b)

# 힘 벡터 (경첩 가까이)
draw_arrow(ax7b, (1.5, 4), (1.5, 7), RED, r'$\vec{F}$', (0.5, 0), fontsize=16, lw=3)

# 거리 표시
ax7b.annotate('', xy=(1.5, 0.2), xytext=(0, 0.2),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=2))
ax7b.text(0.75, -0.3, r"$r'$ (small)", fontsize=14, color=BLUE, ha='center')

ax7b.text(5, -0.9, r"$\tau' = r'F$ (Small torque)", fontsize=14, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/torque_07_door.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("torque_07_door.png 생성 완료")

# ============================================
# 8. 자전거 페달 최적 위치
# ============================================
fig8, ax8 = plt.subplots(figsize=(10, 10))
setup_clean_ax(ax8, (-5, 5), (-5, 5))
ax8.set_title('Bicycle Pedal - Optimal Force Direction', fontsize=16, fontweight='bold', pad=10)

# 크랭크 축 (중심)
crank_center = (0, 0)
ax8.plot(*crank_center, 'ko', markersize=20)
ax8.plot(*crank_center, 'wo', markersize=10)

# 크랭크 암 (회전)
crank_length = 3
# 3시 방향 (최적 위치)
pedal_pos = (crank_length, 0)
ax8.plot([0, pedal_pos[0]], [0, pedal_pos[1]], color=GRAY, lw=8, solid_capstyle='round')

# 페달
pedal = FancyBboxPatch((pedal_pos[0]-0.3, pedal_pos[1]-0.6), 0.6, 1.2, 
                        boxstyle="round,pad=0.05", facecolor='black', edgecolor='gray', lw=2)
ax8.add_patch(pedal)

# 힘 벡터 (아래로 - 최적)
draw_arrow(ax8, pedal_pos, (pedal_pos[0], pedal_pos[1]-2.5), RED, r'$\vec{F}$', (0.5, 0), fontsize=18, lw=4)

# r 벡터
draw_arrow(ax8, crank_center, (pedal_pos[0]-0.1, pedal_pos[1]), BLUE, r'$\vec{r}$', (0, 0.5), fontsize=16, lw=2)

# 직각 표시
rect = patches.Rectangle((2.6, -0.4), 0.4, 0.4, fill=False, edgecolor=ORANGE, lw=2)
ax8.add_patch(rect)

# 회전 방향
rotation_arc = Arc(crank_center, 5, 5, angle=0, theta1=270, theta2=360, color=GREEN, lw=3, linestyle='--')
ax8.add_patch(rotation_arc)
ax8.annotate('', xy=(1.5, -2.5), xytext=(2, -2.3),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=2))

# 다른 위치의 페달 (비효율적)
# 12시 위치
ax8.plot([0, 0], [0, 2.5], color=GRAY, lw=4, alpha=0.3, solid_capstyle='round')
ax8.plot(0, 2.5, 'o', markersize=10, color=GRAY, alpha=0.5)
ax8.annotate('', xy=(0, 1.5), xytext=(0, 2.5),
            arrowprops=dict(arrowstyle='->', color=RED, lw=2, alpha=0.4))
ax8.text(-1.2, 2.5, r'$\tau = 0$', fontsize=12, color=GRAY, alpha=0.7)

# 설명
ax8.text(0, 4, r'$\theta = 90°$ at 3 o\'clock position', fontsize=14, ha='center')
ax8.text(0, 3.3, r'$\tau = rF\sin(90°) = rF_{max}$', fontsize=16, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

ax8.text(0, -4, 'Force perpendicular to crank = Maximum torque', fontsize=13, ha='center', 
         style='italic', color=GRAY)

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/torque_08_pedal.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("torque_08_pedal.png 생성 완료")

print("\n모든 돌림힘 다이어그램 생성 완료!")
print("생성된 파일:")
print("  - torque_01_basic.png      : 돌림힘 기본 개념")
print("  - torque_02_moment_arm.png : 모멘트 팔 비교")
print("  - torque_03_graph.png      : 각도-돌림힘 그래프")
print("  - torque_04_wrench.png     : 스패너 비교")
print("  - torque_05_seesaw.png     : 시소 평형")
print("  - torque_06_righthand.png  : 오른손 법칙")
print("  - torque_07_door.png       : 문 열기 비교")
print("  - torque_08_pedal.png      : 자전거 페달")


st.pyplot(fig1)
st.pyplot(fig2)
st.pyplot(fig3)
st.pyplot(fig4)
st.pyplot(fig5)
st.pyplot(fig6)
st.pyplot(fig7)
st.pyplot(fig8)