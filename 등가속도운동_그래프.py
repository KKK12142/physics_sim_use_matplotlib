from utils import Rope
from utils import MassPoint
from utils import *
import streamlit as st
import numpy as np

setup_style('AppleGothic')  # Mac

fig, ax = plt.subplots(figsize=(8, 6))
clean_ax(ax, (0, 10), (0, 10))
ax.set_xticks(range(-2, 11, 2))
ax.set_yticks(range(-2, 11, 2))
# on= 으로 자동 스냅
g = Ground(ax, y=0, xlim=(-2, 8))

incl1 = Incline(ax, origin = (0, 0), width = 3.5, height = 2, color = "orange", direction="+")
incl2 = Incline(ax, origin = (3.5, 0), width = 2, height = 2, color = "orange", direction="-")
b1 = Box(ax, size=(0.7, 0.4), on=incl1, color="blue", t = 0.6)
b2 = Box(ax, size=(0.7, 0.4), on=incl2, color="red", t = 0.6)
c1 = Circle(ax, radius=0.2, color="green", on=incl1, t=0.2)
b3 = Box(ax, size=(1, 1), color= "black", x=-2, y=0)
r = Rope(ax, b1.right, b2.left )

mg_magnitude = 1.5       
mg = Point(0, -mg_magnitude)
N_magnitude = mg_magnitude * np.cos(incl1.angle_rad)
N = b1.surface_normal * N_magnitude 

F_net = mg + N
arrow(ax, b1.center, b1.center + mg, RED, label=r'$\vec{mg}$')
arrow(ax, b1.center, b1.center + N, RED, label=r'$\vec{N}$')
arrow(ax, b1.center, b1.center + F_net, RED, label=r'$\vec{F_net}$')

st.pyplot(fig)