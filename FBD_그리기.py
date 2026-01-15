from numpy import rad2deg
from PIL._imaging import font
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import streamlit as st

# 스타일 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.unicode_minus'] = False

# 색상 팔레트
BLUE = '#2563eb'
RED = '#dc2626'
GREEN = '#16a34a'
ORANGE = '#ea580c'
PURPLE = '#7c3aed'
GRAY = '#6b7280'
BROWN = '#92400e'

#figure들 리스트에 저장
figures = []

def draw_arrow(ax, start, end, color, label='', label_offset=(0.3, 0), fontsize=12, lw=2.5):
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
    ax.set_xticks([])
    ax.set_yticks([])

# ============================================
# 1. 자유물체도 개념 - 실제 상황 vs 자유물체도
# ============================================
fig1, (ax1a, ax1b) = plt.subplots(1, 2, figsize=(12, 4))

# 왼쪽: 실제 상황
setup_clean_ax(ax1a, (-2, 8), (-1, 6))

ax1a.set_title('바닥에 상자가 올려진 상황', fontsize=24, fontweight='bold', pad=10)

# 바닥
ax1a.fill_between([-2, 8], [-0.5, -0.5], [0, 0], color='#d4a574', alpha=0.7)
ax1a.plot([-2, 8], [0, 0], 'k-', lw=2)
ax1b.fill_between([-2, 8], [-0.5, -0.5], [0, 0], color='#d4a574', alpha=0.7)
ax1b.plot([-2, 8], [0, 0], 'k-', lw=2)

# 빗금
for i in range(-2, 8):
    ax1a.plot([i, i+0.5], [0, -0.5], 'k-', lw=0.5)
    ax1b.plot([i, i+0.5], [0, -0.5], 'k-', lw=0.5)

# 상자
box_w, box_h = 2, 1.5
boxa = patches.FancyBboxPatch((2, 0), box_w, box_h, boxstyle="round,pad=0.05",
                               facecolor='lightblue', edgecolor='black', lw=2)
ax1a.add_patch(boxa)
ax1a.text(2+box_w/2, box_h/2, '상자', fontsize=12, ha='center', va='center')

boxb = patches.FancyBboxPatch((2, 0), box_w, box_h, boxstyle="round,pad=0.05",
                               facecolor='lightblue', edgecolor='black', lw=2)
ax1b.add_patch(boxb)
ax1b.text(2+box_w/2, box_h/2, '', fontsize=12, ha='center', va='center')

# 오른쪽: 자유물체도
setup_clean_ax(ax1b, (-2, 8), (-1, 6))
ax1b.set_title('이 물체의 자유물체도를 그리면', fontsize=24, fontweight='bold', pad=10)

# 점으로 표현된 물체
ax1b.plot(2 + box_w/2, box_h/2 , 'ko', markersize=15)

# 힘 벡터들
draw_arrow(ax1b, (2 + box_w/2, box_h/2), (2 + box_w/2, box_h/2 + 2), RED, '수직항력', (2.4, 0), fontsize=16 )      # 수직항력
draw_arrow(ax1b, (2 + box_w/2, box_h/2), (2 + box_w/2, box_h/2 - 2), BLUE, '중력', (2.4, -1), fontsize=16)     # 중력
ax1a.set_ylim(-4, 6)
ax1b.set_ylim(-4, 6)
plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/fbd_01_concept.png', dpi=150, bbox_inches='tight')
plt.close()
figures.append(fig1)

# ============================================
# 2. 바닥 위 정지한 물체
# ============================================
fig2, ax2 = plt.subplots(figsize=(6, 6))
setup_clean_ax(ax2, (-3, 3), (-3, 4))
ax2.set_title('바닥 위 평형상태의 물체', fontsize=14, fontweight='bold', pad=10)

# 물체 (사각형으로 표현)
box = patches.Rectangle((-0.8, -0.5), 1.6, 1, facecolor='lightgray', 
                         edgecolor='black', lw=2)
ax2.add_patch(box)
ax2.text(0, 0, 'm', fontsize=14, ha='center', va='center')

# 힘 벡터들
draw_arrow(ax2, (0, 0.5), (0, 2.5), RED, r'$\vec{N}$', (0.5, 0), lw=3, fontsize=20)
draw_arrow(ax2, (0, -0.5), (0, -2.5), BLUE, r'$\vec{W} = m\vec{g}$', (1.0, 0), lw=3, fontsize=20)

# 설명
ax2.text(0, 3.3, r'$\vec{N} + \vec{W} = 0$', fontsize=14, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/fbd_02_floor.png', dpi=150, bbox_inches='tight')
plt.close()
figures.append(fig2)

# ============================================
# 3. 경사면 위 물체
# ============================================

fig3, ax3 = plt.subplots(figsize=(8, 6))
setup_clean_ax(ax3, (-1, 9), (-1, 6))
ax3.set_title('경사면에 놓인 물체', fontsize=20, fontweight='bold', pad=10)

# 경사면
incline_x = [0, 8, 0, 0]
incline_y = [0, 0, 4, 0]
ax3.fill(incline_x, incline_y, color='#d4a574', alpha=0.5)

ax3.plot([0, 8], [0, 0], 'k-', lw=2)
ax3.plot([0, 0], [0, 4], 'k-', lw=2)
ax3.plot([0, 8], [4, 0], 'k-', lw=2)
ax3.plot(0, 0, 'ro', markersize=12)

# 각도 표시
angle_arc = patches.Arc((8, 0), 2, 2, angle=0, theta1=180-26.56, theta2=180, color=ORANGE, lw=3)
ax3.add_patch(angle_arc)
ax3.text(6.5, 0.2, r'$\theta$', fontsize=18, color=ORANGE)

# 물체 위치 (경사면 중간)
rect = patches.Rectangle((4-1, 2+0.5), 2, 1, angle=-26.56, color='lightgray', alpha=0.7)
ax3.add_patch(rect)
obj_x, obj_y = 4, 2.5
ax3.plot(obj_x, obj_y, 'ko', markersize=12)

# 좌표계 표시 (경사면 기준)
ax3.annotate('', xy=(obj_x+1.5, obj_y-0.75), xytext=(obj_x, obj_y),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
ax3.text(obj_x+1.7, obj_y-0.6, "x'", fontsize=11, color=GRAY)
ax3.annotate('', xy=(obj_x+0.75, obj_y+1.5), xytext=(obj_x, obj_y),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
ax3.text(obj_x+0.5, obj_y+1.7, "y'", fontsize=11, color=GRAY)

# 힘 벡터들
# 수직항력 (경사면에 수직)
draw_arrow(ax3, (obj_x, obj_y), (obj_x+0.75, obj_y+1.5), RED, r'$\vec{N}$', (0.5, 0.3), lw=3)

# 중력 (아래로)
draw_arrow(ax3, (obj_x, obj_y), (obj_x, obj_y-2), BLUE, r'$\vec{W}$', (-0.5, 0), lw=3)

# # 중력 성분 (점선)
# ax3.plot([obj_x, obj_x+1], [obj_y-2, obj_y-2-0.5], 'b--', lw=1.5, alpha=0.7)
# ax3.plot([obj_x, obj_x+1], [obj_y-2, obj_y-2+0.0], 'b--', lw=1.5, alpha=0.7)

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/fbd_03_incline.png', dpi=150, bbox_inches='tight')
plt.close()

figures.append(fig3)
# ============================================
# 4. 경사면 - 힘의 분해
# ============================================

fig4, ax4 = plt.subplots(figsize=(7, 7))
setup_clean_ax(ax4, (-4, 4), (-4, 4))
ax4.set_title('경사면위 물체가 받는 힘의 분해', fontsize=20, fontweight='bold', pad=10)

# 물체
ax4.plot(0, 0, 'ko', markersize=15)

# 경사면 방향 좌표축 (회전된)
theta = np.radians(26.56)
ax4.annotate('', xy=(3*np.cos(theta), -3*np.sin(theta)), xytext=(-3*np.cos(theta), 3*np.sin(theta)),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
ax4.text(3.2*np.cos(theta), -3.2*np.sin(theta), "x' (along slope)", fontsize=10, color=GRAY)

ax4.annotate('', xy=(3*np.sin(theta), 3*np.cos(theta)), xytext=(-3*np.sin(theta), -3*np.cos(theta)),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
ax4.text(2.5*np.sin(theta)+0.3, 3*np.cos(theta), "y' (⊥ slope)", fontsize=10, color=GRAY)

# 중력 (수직 아래)
W = 2.5
draw_arrow(ax4, (0, 0), (0, -W), BLUE, r'$\vec{W}$', (-0.3, -0.3), lw=3)

# 중력의 성분들
Wx = W * np.sin(theta)  # 경사면 방향
Wy = W * np.cos(theta)  # 경사면 수직 방향

# W의 x' 성분 (경사면 따라 내려가는 방향)
draw_arrow(ax4, (0, 0), (Wx*np.cos(theta), -Wx*np.sin(theta)), GREEN, 
           r"$W_{x'} = mg\sin\theta$", (1.2, 0), lw=2.5)

# W의 y' 성분 (경사면 누르는 방향)  
draw_arrow(ax4, (0, 0), (-Wy*np.sin(theta), -Wy*np.cos(theta)), PURPLE,
           r"$W_{y'} = mg\cos\theta$", (-1.1, 0), lw=2.5)

# 점선으로 평행사변형
end_Wx = (Wx*np.cos(theta), -Wx*np.sin(theta))
end_Wy = (-Wy*np.sin(theta), -Wy*np.cos(theta))
ax4.plot([end_Wx[0], 0], [end_Wx[1], -W], 'k--', lw=1, alpha=0.5)
ax4.plot([end_Wy[0], 0], [end_Wy[1], -W], 'k--', lw=1, alpha=0.5)

# 수직항력
draw_arrow(ax4, (0, 0), (Wy*np.sin(theta), Wy*np.cos(theta)), RED,
           r'$\vec{N}$', (0.5, 0.3), lw=3)

# 각도 표시
angle_arc = patches.Arc((0, 0), 1.2, 1.2, angle=-(90+26.65), theta1=0, theta2=rad2deg(theta), color=ORANGE, lw=2)
ax4.add_patch(angle_arc)
ax4.text(-0.3, -1, r'$\theta$', fontsize=14,  color=ORANGE)

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/fbd_04_decomposition.png', dpi=150, bbox_inches='tight')
plt.close()
figures.append(fig4)

# ============================================
# 5. 줄에 매달린 물체
# ============================================
fig5, ax5 = plt.subplots(figsize=(6, 7))
setup_clean_ax(ax5, (-3, 3), (-4, 3))
ax5.set_title('Hanging Object', fontsize=14, fontweight='bold', pad=10)

# 천장
ax5.plot([-2, 2], [2, 2], 'k-', lw=3)
for i in range(-2, 2):
    ax5.plot([i, i+0.3], [2, 2.3], 'k-', lw=1)

# 밧줄 색상
ROPE_COLOR = '#8B4513'  # 갈색 (SaddleBrown)

# 줄 (두께감 표현)
rope_width = 0.08
ax5.fill_betweenx([0.5, 2], -rope_width, rope_width, color=ROPE_COLOR, alpha=0.8)

# 밧줄 빗금 (꼬임 표현)
for y in np.arange(0.6, 2, 0.15):
    ax5.plot([-rope_width, rope_width], [y, y + 0.1], color='#5D3A1A', lw=1)

# 줄 테두리
ax5.plot([-rope_width, -rope_width], [0.5, 2], color='#5D3A1A', lw=1)
ax5.plot([rope_width, rope_width], [0.5, 2], color='#5D3A1A', lw=1)

# 물체
circle = patches.Circle((0, 0), 0.5, facecolor='lightblue', edgecolor='black', lw=2)
ax5.add_patch(circle)
ax5.text(0, 0, 'm', fontsize=14, ha='center', va='center')

# 힘 벡터들
draw_arrow(ax5, (0, 0), (0, 2.5), RED, r'$\vec{T}$', (0.5, 0), lw=3)
draw_arrow(ax5, (0, 0), (0, -2.5), BLUE, r'$\vec{W}$', (0.5, 0), lw=3)

# 평형 조건
ax5.text(0, -3.5, r'$\vec{T} + \vec{W} = 0$  →  $T = mg$', fontsize=13, ha='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/fbd_05_hanging.png', dpi=150, bbox_inches='tight')
plt.close()
figures.append(fig5)

# ============================================
# 6. 마찰력이 있는 경우 (밀고 있는 상자)
# ============================================
fig6, ax6 = plt.subplots(figsize=(8, 6))
setup_clean_ax(ax6, (-4, 6), (-3, 4))
ax6.set_title('오른쪽으로 미는 상자(마찰력 O)', fontsize=20, fontweight='bold', pad=10)

# 물체
box = patches.Rectangle((-1, -0.75), 2, 1.5, facecolor='lightgray', 
                         edgecolor='black', lw=2)
ax6.add_patch(box)
ax6.text(0, 0, 'm', fontsize=14, ha='center', va='center')

# 바닥 표시
ax6.plot([-4, 6], [-0.75, -0.75], 'k-', lw=2)

# 힘 벡터들
draw_arrow(ax6, (0, 0.75), (0, 2.5), RED, r'$\vec{N}$', (0.5, 0), lw=3)
draw_arrow(ax6, (0, -0.75), (0, -2.5), BLUE, r'$\vec{W}$', (0.5, 0), lw=3)
draw_arrow(ax6, (1, 0), (3, 0), GREEN, r'$\vec{F}$', (0, 0.4), lw=3)  # 미는 힘
draw_arrow(ax6, (-1, 0), (-2.5, 0), ORANGE, r'$\vec{f}$', (0, 0.4), lw=3)  # 마찰력

# 범례 설명
ax6.text(0, 3.3, r'$\vec{F}$: 작용하는 힘    $\vec{f}$: 마찰력', fontsize=14, ha='center')

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/fbd_06_friction.png', dpi=150, bbox_inches='tight')
plt.close()
figures.append(fig6)

# ============================================
# 7. 두 물체 연결 (도르래)
# ============================================
fig7, ax7 = plt.subplots(figsize=(8, 7))
setup_clean_ax(ax7, (-2, 10), (-5, 3))
ax7.set_title('도르레로 연결된 두 물체', fontsize=20, fontweight='bold', pad=5)

# 도르래
pulley = patches.Circle((4, 0.25), 0.25, facecolor='white', edgecolor='black', lw=2)
ax7.add_patch(pulley)

# 테이블
ax7.fill_between([0, 3.5], [-4.5, -4.5], [0, 0], color='#d4a574', alpha=0.7)
ax7.plot([0, 3.5], [0, 0], 'k-', lw=2)
ax7.plot([3.5, 3.5], [0, -4.5], 'k-', lw=2)

# 물체 1 (테이블 위)
box1 = patches.Rectangle((1.5, 0), 1.5, 1, facecolor='lightblue', edgecolor='black', lw=2)
ax7.add_patch(box1)
ax7.text(2.25, 0.5, r'$m_1$', fontsize=12, ha='center', va='center')

# 줄
ax7.plot([3, 4], [0.5, 0.5], 'k-', lw=2)
ax7.plot([3.5, 4], [0, 0.25], 'k-', lw=2)
ax7.plot([4.25, 4.25], [0.25, -2], 'k-', lw=2)

# 물체 2 (매달린)
box2 = patches.Rectangle((3.75, -3.5), 1, 1.5, facecolor='lightcoral', edgecolor='black', lw=2)
ax7.add_patch(box2)
ax7.text(4.25, -2.75, r'$m_2$', fontsize=12, ha='center', va='center')

# 물체 1의 자유물체도
ax7.text(7, 1.5, r'FBD of $m_1$:', fontsize=11, fontweight='bold')
ax7.plot(7.5, 0, 'ko', markersize=10)
draw_arrow(ax7, (7.5, 0), (9, 0), RED, r'$\vec{T}$', (0, 0.3), lw=2)
draw_arrow(ax7, (7.5, 0), (7.5, 1), GREEN, r'$\vec{N}$', (0.4, 0), lw=2)
draw_arrow(ax7, (7.5, 0), (7.5, -1), BLUE, r'$\vec{W}_1$', (0.5, 0), lw=2)

# 물체 2의 자유물체도
ax7.text(7, -2, r'FBD of $m_2$:', fontsize=11, fontweight='bold')
ax7.plot(7.5, -3.5, 'ko', markersize=10)
draw_arrow(ax7, (7.5, -3.5), (7.5, -2.5), RED, r'$\vec{T}$', (0.4, 0), lw=2)
draw_arrow(ax7, (7.5, -3.5), (7.5, -4.5), BLUE, r'$\vec{W}_2$', (0.5, 0), lw=2)

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/fbd_07_pulley.png', dpi=150, bbox_inches='tight')
plt.close()
figures.append(fig7)

# ============================================
# 8. 자유물체도 그리기 단계
# ============================================
fig8, axes = plt.subplots(1, 4, figsize=(14, 4))

titles = ['Step 1: Isolate', 'Step 2: Point Mass', 'Step 3: Forces', 'Step 4: Label']

for i, ax in enumerate(axes):
    setup_clean_ax(ax, (-2, 2), (-2, 2))
    ax.set_title(titles[i], fontsize=11, fontweight='bold', pad=5)

box1 = patches.Rectangle((-0.5, -0.5), 1, 1, facecolor='lightblue', 
                                     edgecolor='black', lw=2, linestyle='--')
box2 = patches.Rectangle((-0.5, -0.5), 1, 1, facecolor='lightblue', 
                                     edgecolor='black', lw=2, linestyle='--')
box3 = patches.Rectangle((-0.5, -0.5), 1, 1, facecolor='lightblue', 
                                     edgecolor='black', lw=2, linestyle='--')
box4 = patches.Rectangle((-0.5, -0.5), 1, 1, facecolor='lightblue', 
                                     edgecolor='black', lw=2, linestyle='--')

# Step 1: 물체 분리
axes[0].add_patch(box1)
axes[0].text(0, 0, '?', fontsize=16, ha='center', va='center')

# Step 2: 점으로 표현
axes[1].add_patch(box2)
axes[1].plot(0, 0, 'ko', markersize=15)

# Step 3: 힘 화살표
axes[2].add_patch(box3)
axes[2].plot(0, 0, 'ko', markersize=15)
draw_arrow(axes[2], (0, 0), (0, 1.3), RED, r'$\vec{N}$', (0.4, +0.5), lw=2)
draw_arrow(axes[2], (0, 0), (0, -1.3), BLUE, r'$\vec{W}$', (0.5, -0.5), lw=2)

# Step 4: 라벨 추가
axes[3].add_patch(box4)
axes[3].plot(0, 0, 'ko', markersize=15)

draw_arrow(axes[3], (0, 0), (0, 1.3), RED, r'$\vec{N}$', (0.4, +0.5), lw=2)
draw_arrow(axes[3], (0, 0), (0, -1.3), BLUE, r'$\vec{mg}$', (0.5, -0.5), lw=2)

# axes[3].text(0.3, 1, r'$\vec{N}$', fontsize=12, color=RED, fontweight='bold')
# axes[3].text(0.3, -1, r'$\vec{W}$', fontsize=12, color=BLUE, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/fbd_08_steps.png', dpi=150, bbox_inches='tight')
plt.close()

figures.append(fig8)

print("All FBD diagrams created successfully!")
print("Files saved:")
print("  fbd_01_concept.png      - 개념 비교")
print("  fbd_02_floor.png        - 바닥 위 물체")
print("  fbd_03_incline.png      - 경사면 위 물체")
print("  fbd_04_decomposition.png - 힘의 분해")
print("  fbd_05_hanging.png      - 매달린 물체")
print("  fbd_06_friction.png     - 마찰력")
print("  fbd_07_pulley.png       - 도르래")
print("  fbd_08_steps.png        - 그리기 단계")

for fig in figures:
    st.pyplot(fig)