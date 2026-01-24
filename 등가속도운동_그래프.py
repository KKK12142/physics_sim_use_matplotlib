from utils import *
import streamlit as st
import numpy as np

setup_style('AppleGothic')  # Mac

# ============================================
# 테스트 1: 테이블 + 도르래
# ============================================
st.header("테스트 1: 테이블 양끝 도르래")

fig, ax = plt.subplots(figsize=(10, 6))
clean_ax(ax, (-2, 10), (-2, 5))

# 테이블 생성
table = Table(ax, x=1, y=2, width=6, height=1)

# 테이블 위에 박스
box = Box(ax, size=(1.2, 0.8), on=table, t=0.5, label='m', color='lightblue')

# 도르래: 자동으로 크기와 위치 결정 (for_obj 기준)
p_left = Pulley(ax, on=table, t=0, for_obj=box)
p_right = Pulley(ax, on=table, t=1, for_obj=box)

# 매달린 추
box_left = Box(ax, x=p_left.bottom.x, y=2, size=(0.6, 0.8), label='M1', color='orange')
box_right = Box(ax, x=p_right.bottom.x, y=1, size=(0.6, 0.8), label='M2', color='green')


# 로프 연결
Rope(ax, box.left, p_left.right)          # 박스 왼쪽 → 도르래 오른쪽
Rope(ax, p_left.bottom, box_left.top)  # 도르래 아래로

Rope(ax, box.right, p_right.left)         # 박스 오른쪽 → 도르래 왼쪽
Rope(ax, p_right.bottom, box_right.top)  # 도르래 아래로


st.pyplot(fig)

# ============================================
# 테스트 2: 경사면 + 도르래
# ============================================
st.header("테스트 2: 경사면 끝 도르래")

fig2, ax2 = plt.subplots(figsize=(10, 6))
clean_ax(ax2, (-1, 10), (-1, 6))

# 경사면 생성
incline = Incline(ax2, origin=(0, 0), width=6, height=3, direction='-', color='#d4a574')

# 경사면 위에 박스
box_incline = Box(ax2, size=(1, 0.6), on=incline, t=0.4, label='m', color='lightblue')

# 도르래: 경사면 왼쪽 끝 (낮은 곳, + direction이므로)
pulley = Pulley(ax2, on=incline, t=0, for_obj=box_incline)

# 로프 연결: 박스 left → 도르래 right → 아래 추
Rope(ax2, box_incline.left, pulley.right)
Rope(ax2, pulley.bottom, (pulley.bottom.x, 0))

# 매달린 추
hanging_box = Box(ax2, x=pulley.bottom.x, y=0.5, size=(0.4, 1), label='M', color='orange')

st.pyplot(fig2)

# ============================================
# 테스트 3: 반대 방향 경사면
# ============================================
st.header("테스트 3: 반대 방향 경사면 (+ direction)")

fig3, ax3 = plt.subplots(figsize=(10, 6))
clean_ax(ax3, (-1, 10), (-1, 6))

# 경사면 생성 (+ 방향: 오른쪽 위로)
incline2 = Incline(ax3, origin=(0, 0), width=6, height=3, direction='+', color='#d4a574')

# 경사면 위에 박스
box_incline2 = Box(ax3, size=(1, 0.6), on=incline2, t=0.6, label='m', color='lightblue')

# 도르래: 경사면 오른쪽 끝 (낮은 곳, - direction이므로)
pulley2 = Pulley(ax3, on=incline2, t=1, for_obj=box_incline2)

# 로프 연결: 박스 right → 도르래 left
Rope(ax3, box_incline2.right, pulley2.left)
Rope(ax3, pulley2.bottom, (pulley2.bottom.x, 0))

# 매달린 추
hanging_box2 = Box(ax3, x=pulley2.bottom.x, y=0.5, size=(0.8, 1), label='M', color='orange')

st.pyplot(fig3)
