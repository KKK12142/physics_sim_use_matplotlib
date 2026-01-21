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
# 1. 같은 방향으로 힘이 작용하는 경우
# ============================================
fig1, ax1 = plt.subplots(figsize=(10, 6))
setup_clean_ax(ax1, (-1, 12), (-3, 4))

# 물체 (상자)
box_w, box_h = 1.5, 1.2
box = patches.FancyBboxPatch((0, -box_h/2), box_w, box_h, 
                              boxstyle="round,pad=0.05",
                              facecolor='lightgray', edgecolor='black', lw=2)
ax1.add_patch(box)
ax1.text(box_w/2, 0, 'm', fontsize=16, ha='center', va='center', fontweight='bold')

# F1 화살표 (오른쪽)
F1_start = (box_w, 0.2)
F1_end = (box_w + 3, 0.2)
draw_arrow(ax1, F1_start, F1_end, BLUE, '', (0, 0), fontsize=18, lw=4)
ax1.text(F1_end[0] + 0.3, F1_end[1], r'$\vec{F}_1$', fontsize=20, color=BLUE, 
         fontweight='bold', va='center')

# F2 화살표 (오른쪽, 약간 아래)
F2_start = (box_w, -0.2)
F2_end = (box_w + 2, -0.2)
draw_arrow(ax1, F2_start, F2_end, RED, '', (0, 0), fontsize=18, lw=4)
ax1.text(F2_end[0] + 0.3, F2_end[1], r'$\vec{F}_2$', fontsize=20, color=RED, 
         fontweight='bold', va='center')

# 알짜힘 (합력) - 아래쪽에 표시
ax1.plot([0.75, 0.75], [-1.2, -1.8], 'k--', lw=1, alpha=0.5)

Fnet_start = (0.75, -2)
Fnet_end = (0.75 + 5, -2)
draw_arrow(ax1, Fnet_start, Fnet_end, GREEN, '', (0, 0), fontsize=18, lw=4)
ax1.text(Fnet_end[0] + 0.3, Fnet_end[1], r'$\vec{F}_{net}$', fontsize=20, color=GREEN, 
         fontweight='bold', va='center')

# 수식 표시
ax1.text(6, 2.5, r'$\vec{F}_{net} = \vec{F}_1 + \vec{F}_2$', fontsize=22, 
         ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                   edgecolor='gray', alpha=0.9))

# 방향 표시
ax1.annotate('', xy=(10, 0), xytext=(9, 0),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=2))
ax1.text(10.3, 0, '+x방향', fontsize=14, color=GRAY, va='center')

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/같은방향힘.png', dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.close()

print("같은방향힘이.png 생성 완료")

# ============================================
# 2. 반대 방향으로 힘이 작용하는 경우
# ============================================
fig2, ax2 = plt.subplots(figsize=(10, 6))
setup_clean_ax(ax2, (-5, 8), (-3, 4))

# 물체 (상자)
box = patches.FancyBboxPatch((0, -box_h/2), box_w, box_h, 
                              boxstyle="round,pad=0.05",
                              facecolor='lightgray', edgecolor='black', lw=2)
ax2.add_patch(box)
ax2.text(box_w/2, 0, 'm', fontsize=16, ha='center', va='center', fontweight='bold')

# F1 화살표 (오른쪽, 더 큰 힘)
F1_start = (box_w, 0)
F1_end = (box_w + 4, 0)
draw_arrow(ax2, F1_start, F1_end, BLUE, '', (0, 0), fontsize=18, lw=4)
ax2.text(F1_end[0] + 0.3, F1_end[1], r'$\vec{F}_1$', fontsize=20, color=BLUE, 
         fontweight='bold', va='center')

# F2 화살표 (왼쪽, 더 작은 힘)
F2_start = (0, 0)
F2_end = (-2.5, 0)
draw_arrow(ax2, F2_start, F2_end, RED, '', (0, 0), fontsize=18, lw=4)
ax2.text(F2_end[0] - 0.5, F2_end[1], r'$\vec{F}_2$', fontsize=20, color=RED, 
         fontweight='bold', va='center')

# 알짜힘 (합력) - 아래쪽에 표시
ax2.plot([0.75, 0.75], [-1.2, -1.8], 'k--', lw=1, alpha=0.5)

Fnet_start = (0.75, -2)
Fnet_end = (0.75 + 1.5, -2)  # F1 - F2 = 4 - 2.5 = 1.5
draw_arrow(ax2, Fnet_start, Fnet_end, GREEN, '', (0, 0), fontsize=18, lw=4)
ax2.text(Fnet_end[0] + 0.3, Fnet_end[1], r'$\vec{F}_{net}$', fontsize=20, color=GREEN, 
         fontweight='bold', va='center')

# 수식 표시
ax2.text(3, 2.5, r'$\vec{F}_{net} = \vec{F}_1 + \vec{F}_2$', fontsize=22, 
         ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                   edgecolor='gray', alpha=0.9))

# 크기 비교 설명 (영어로)
ax2.text(3, 1.5, r'($|\vec{F}_1| > |\vec{F}_2|$)', fontsize=16, 
         ha='center', va='center', color=GRAY)

# 방향 표시
ax2.annotate('', xy=(7, -1), xytext=(6, -1),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=2))
ax2.text(7.3, -1, '+x방향', fontsize=14, color=GRAY, va='center')

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/반대방향힘.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("반대방향힘.png 생성 완료")

# ============================================
# 3. 힘의 단위 설명 이미지 (보너스)
# ============================================
fig3, ax3 = plt.subplots(figsize=(10, 5))
setup_clean_ax(ax3, (-1, 11), (-1, 5))

# 1N = 1kg × 1m/s² 설명
ax3.text(5, 4, r'$1\,\mathrm{N} = 1\,\mathrm{kg} \cdot \mathrm{m/s}^2$', 
         fontsize=28, ha='center', va='center', fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', 
                   edgecolor='navy', alpha=0.8))

# 물체와 힘 시각화
# 1kg 물체
box = patches.FancyBboxPatch((1, 0.5), 2, 1.5, boxstyle="round,pad=0.05",
                              facecolor='lightgray', edgecolor='black', lw=2)
ax3.add_patch(box)
ax3.text(2, 1.25, '1 kg', fontsize=14, ha='center', va='center', fontweight='bold')

# 1N 힘 화살표
draw_arrow(ax3, (3, 1.25), (5.5, 1.25), BLUE, '1 N', (0, 0.5), fontsize=16, lw=4)

# 가속도 표시
ax3.text(7.5, 1.25, r'$\rightarrow\, a = 1\,\mathrm{m/s}^2$', 
         fontsize=16, ha='left', va='center')

# 뉴턴의 제2법칙 공식
ax3.text(5, -0.3, r'$\vec{F} = m\vec{a}$', fontsize=24, ha='center', va='center',
         color=PURPLE, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/힘의단위.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("힘의단위.png 생성 완료")

# ============================================
# 4. 2차원 힘의 합성 이미지
# ============================================
fig4, ax4 = plt.subplots(figsize=(8, 8))
setup_clean_ax(ax4, (-1, 7), (-1, 5))

# 원점에 물체
circle = patches.Circle((0, 0), 0.3, facecolor='lightgray', edgecolor='black', lw=2)
ax4.add_patch(circle)
ax4.text(0, 0, 'm', fontsize=12, ha='center', va='center', fontweight='bold')

# F1 (x방향)
F1x, F1y = 4, 0
draw_arrow(ax4, (0, 0), (F1x, F1y), BLUE, r'$\vec{F}_1$', (0, 0.4), fontsize=16, lw=3)

# F2 (y방향)
F2x, F2y = 0, 3
draw_arrow(ax4, (0, 0), (F2x, F2y), RED, r'$\vec{F}_2$', (-0.5, 0), fontsize=16, lw=3)

# 합력 (대각선)
Fnet_x, Fnet_y = F1x + F2x, F1y + F2y
draw_arrow(ax4, (0, 0), (Fnet_x, Fnet_y), GREEN, r'$\vec{F}_{net}$', (0.5, 0.3), fontsize=16, lw=4)

# 점선으로 평행사변형
ax4.plot([F1x, Fnet_x], [F1y, Fnet_y], 'k--', lw=1.5, alpha=0.5)
ax4.plot([F2x, Fnet_x], [F2y, Fnet_y], 'k--', lw=1.5, alpha=0.5)

# 직각 표시
right_angle = patches.Rectangle((0, 0), 0.4, 0.4, fill=False, edgecolor=GRAY, lw=1)
ax4.add_patch(right_angle)

# 각도 표시
angle = np.degrees(np.arctan2(Fnet_y, Fnet_x))
angle_arc = patches.Arc((0, 0), 1.5, 1.5, angle=0, theta1=0, theta2=angle, 
                         color=ORANGE, lw=2)
ax4.add_patch(angle_arc)
ax4.text(1.2, 0.5, r'$\theta$', fontsize=14, color=ORANGE)

# 수식
ax4.text(3.5, 4.5, r'$\vec{F}_{net} = \vec{F}_1 + \vec{F}_2$', fontsize=18, 
         ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9))

ax4.text(3.5, 3.7, r'$|\vec{F}_{net}| = \sqrt{F_1^2 + F_2^2}$', fontsize=16, 
         ha='center', va='center', color=GREEN)

# 좌표축
ax4.annotate('', xy=(6.5, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1))
ax4.text(6.7, 0, 'x', fontsize=12, color=GRAY, va='center')
ax4.annotate('', xy=(0, 5), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1))
ax4.text(0, 5, 'y', fontsize=12, color=GRAY, ha='center')

plt.tight_layout()
plt.savefig('/Users/rottenapplea/coding/physics_blog_2025/src/content/posts/physics/img/2차원힘합성.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("2차원힘합성.png 생성 완료")

print("\n모든 이미지 생성 완료!")
print("생성된 파일:")
print("  - 같은방향힘.png")
print("  - 반대방향힘.png")  
print("  - 힘의단위.png")
print("  - 2차원힘합성.png")

st.pyplot(fig1)
st.pyplot(fig2)
st.pyplot(fig3)
st.pyplot(fig4)
