
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.font_manager as fm
import streamlit as st




# 스타일 설정
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['font.size'] = 12
plt.rcParams['axes.unicode_minus'] = False

# 한글 폰트 설정 시도
try:
    plt.rcParams['font.family'] = 'AppleGothic'
except:
    pass

# 색상 팔레트
BLUE = '#2563eb'
RED = '#dc2626'
GREEN = '#16a34a'
ORANGE = '#ea580c'
PURPLE = '#7c3aed'
GRAY = '#6b7280'

def setup_ax(ax, xlim=(-1, 6), ylim=(-1, 5), title=''):
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=10)

fig1, ax1 = plt.subplots(figsize=(8, 6))
setup_ax(ax1, xlim=(-0.5, 6), ylim=(-0.5, 5), title='벡터의 표현')

# 벡터 그리기
start = np.array([1, 1])
end = np.array([5, 4])
ax1.annotate('', xy=end, xytext=start,
            arrowprops=dict(arrowstyle='->', color=BLUE, lw=3))

# 레이블
ax1.plot(*start, 'ko', markersize=8)
ax1.text(start[0]-0.3, start[1]-0.3, '시작점', fontsize=11, ha='right')
ax1.text((start[0]+end[0])/2 + 0.3, (start[1]+end[1])/2 - 0.4, 
         r'$\vec{A}$', fontsize=16, color=BLUE, fontweight='bold')
ax1.text(end[0]+0.2, end[1]+0.2, '끝점', fontsize=11)

# 크기 표시
# ax1.annotate('', xy=(0.8, 1.2), xytext=(4.8, 4.2),
#             arrowprops=dict(arrowstyle='<->', color=GRAY, lw=1.5))


ax1.set_xlabel('x', fontsize=12)
ax1.set_ylabel('y', fontsize=12)

#====
fig2, ax2 = plt.subplots(figsize=(8, 6))
setup_ax(ax2, xlim=(-0.5, 6), ylim=(-0.5, 5), title='벡터의 성분 분해')

# 원점에서 시작하는 벡터
A = np.array([4, 3])
theta = np.arctan2(A[1], A[0])

# 원래 벡터
ax2.annotate('', xy=A, xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color=BLUE, lw=3))
ax2.text(A[0]/2 + 0.3, A[1]/2 + 0.4, r'$\vec{A}$', fontsize=16, color=BLUE, fontweight='bold')

# x 성분
ax2.annotate('', xy=(A[0], 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color=RED, lw=2.5))
ax2.text(A[0]/2, -0.4, r'$A_x = A\cos\theta$', fontsize=12, color=RED, ha='center')

# y 성분
ax2.annotate('', xy=(A[0], A[1]), xytext=(A[0], 0),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.5))
ax2.text(A[0]+0.5, A[1]/2, r'$A_y = A\sin\theta$', fontsize=12, color=GREEN, va='center')

# 점선 (직각 표시용)
ax2.plot([0, A[0]], [A[1], A[1]], 'k--', alpha=0.3, lw=1)
ax2.plot([A[0], A[0]], [0, A[1]], 'k--', alpha=0.3, lw=1)

# 각도 호
angle_arc = patches.Arc((0, 0), 1.5, 1.5, angle=0, theta1=0, 
                         theta2=np.degrees(theta), color=ORANGE, lw=2)
ax2.add_patch(angle_arc)
ax2.text(1.0, 0.4, r'$\theta$', fontsize=14, color=ORANGE)

# 직각 표시
rect_size = 0.3
ax2.plot([A[0]-rect_size, A[0]-rect_size, A[0]], [0, rect_size, rect_size], 
         'k-', lw=1)

ax2.set_xlabel('x', fontsize=12)
ax2.set_ylabel('y', fontsize=12)


#============

fig3, ax3 = plt.subplots(figsize=(6, 6,))

ax3.set_xlim(-10, 10)
ax3.set_ylim(-10, 10)
ax3.spines['bottom'].set_position('center')
ax3.spines['left'].set_position('center')

ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# ax3.set_xticks([])
ax3.set_yticks([])

ax3.annotate('', xy=(5, 0.5), xytext=(0, 0.5), arrowprops=dict(arrowstyle='->', color=BLUE, lw=3))
ax3.text(2.5, 0.8, r'$\vec{v} = 5m/s$', fontsize=16, color=BLUE, fontweight='bold')
rect = patches.Rectangle((-1, 0), 2, 1, linewidth=3, edgecolor='red', facecolor='red')
ax3.add_patch(rect)


plt.tight_layout()
st.pyplot(fig1)
st.pyplot(fig2)
st.pyplot(fig3)