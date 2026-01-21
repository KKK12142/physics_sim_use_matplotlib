"""
Physics Diagram Utilities
클래스 기반 물리 다이어그램 도구

사용 예시:
    g = Ground(ax, y=0, xlim=(-2, 8))
    b = Box(ax, x=3, size=(2, 1.5), on=g, label='m')
    arrow(ax, b.center, b.top + (0, 2), RED, label=r'$\\vec{N}$')
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ============================================
# 색상 팔레트
# ============================================
COLORS = {
    'blue': '#2563eb',
    'red': '#dc2626',
    'green': '#16a34a',
    'orange': '#ea580c',
    'purple': '#7c3aed',
    'gray': '#6b7280',
    'brown': '#92400e',
    'rope': '#8B4513',
    'ground': '#d4a574',
}

# 단축 접근
BLUE = COLORS['blue']
RED = COLORS['red']
GREEN = COLORS['green']
ORANGE = COLORS['orange']
PURPLE = COLORS['purple']
GRAY = COLORS['gray']
BROWN = COLORS['brown']

# ============================================
# 스타일 설정
# ============================================
def setup_style(font_family='AppleGothic'):
    """matplotlib 기본 스타일 설정"""
    plt.rcParams['font.family'] = font_family
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.unicode_minus'] = False


def clean_ax(ax, xlim, ylim):
    """깔끔한 축 설정 (눈금, 테두리 제거)"""
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


# ============================================
# Point 클래스 (벡터 연산 지원)
# ============================================
class Point:
    """2D 점/벡터 - 연산자 오버로딩 지원"""
    
    def __init__(self, x, y=None):
        if y is None:
            # tuple이나 list로 받은 경우
            if isinstance(x, (tuple, list, np.ndarray)):
                self.x, self.y = float(x[0]), float(x[1])
            elif isinstance(x, Point):
                self.x, self.y = x.x, x.y
            else:
                raise ValueError("Point requires (x, y) or Point")
        else:
            self.x, self.y = float(x), float(y)
    
    def __add__(self, other):
        if isinstance(other, (tuple, list)):
            return Point(self.x + other[0], self.y + other[1])
        elif isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        raise TypeError(f"Cannot add Point and {type(other)}")
    
    def __sub__(self, other):
        if isinstance(other, (tuple, list)):
            return Point(self.x - other[0], self.y - other[1])
        elif isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        raise TypeError(f"Cannot subtract Point and {type(other)}")
    
    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        """스칼라 나눗셈"""
        return Point(self.x / scalar, self.y / scalar)

    def __iter__(self):
        """tuple로 언패킹 가능하게"""
        yield self.x
        yield self.y
    
    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"
    
    @property
    def tuple(self):
        return (self.x, self.y)
    
    @property
    def array(self):
        return np.array([self.x, self.y])
    
    def distance_to(self, other):
        other = Point(other)
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def angle_to(self, other):
        """다른 점까지의 각도 (라디안)"""
        other = Point(other)
        return np.arctan2(other.y - self.y, other.x - self.x)


# ============================================
# Transform2D 클래스 (2D 아핀 변환)
# ============================================
class Transform2D:
    """2D 아핀 변환 - 로컬 좌표계 정의

    로컬 좌표계:
    - x' 축: 표면의 접선 방향 (오른쪽이 양의 방향)
    - y' 축: 표면의 법선 방향 (위쪽이 양의 방향)
    - 원점: 표면 위의 기준점
    """

    def __init__(self, origin, angle_rad=0):
        """
        Args:
            origin: 로컬 좌표계의 원점 (월드 좌표)
            angle_rad: 로컬 좌표계의 회전 각도 (라디안, 반시계 방향이 양)
        """
        self.origin = Point(origin)
        self.angle = angle_rad
        self._cos = np.cos(angle_rad)
        self._sin = np.sin(angle_rad)

    def local_to_world(self, local_point):
        """로컬 좌표 -> 월드 좌표 변환"""
        p = Point(local_point)
        # 회전 후 평행이동
        wx = self.origin.x + p.x * self._cos - p.y * self._sin
        wy = self.origin.y + p.x * self._sin + p.y * self._cos
        return Point(wx, wy)

    def world_to_local(self, world_point):
        """월드 좌표 -> 로컬 좌표 변환"""
        p = Point(world_point)
        # 평행이동 후 역회전
        dx = p.x - self.origin.x
        dy = p.y - self.origin.y
        lx = dx * self._cos + dy * self._sin
        ly = -dx * self._sin + dy * self._cos
        return Point(lx, ly)

    @property
    def tangent(self):
        """접선 방향 단위 벡터 (월드 좌표계)"""
        return Point(self._cos, self._sin)

    @property
    def normal(self):
        """법선 방향 단위 벡터 (월드 좌표계)"""
        return Point(-self._sin, self._cos)

    @property
    def angle_deg(self):
        """회전 각도 (도)"""
        return np.degrees(self.angle)


# ============================================
# 기본 물리 객체 클래스
# ============================================
class PhysicsObject:
    """모든 물리 객체의 기본 클래스"""
    
    def __init__(self, ax):
        self.ax = ax
        self._center = Point(0, 0)
        self._width = 0
        self._height = 0
    
    @property
    def center(self):
        return self._center
    
    @property
    def top(self):
        return Point(self._center.x, self._center.y + self._height / 2)
    
    @property
    def bottom(self):
        return Point(self._center.x, self._center.y - self._height / 2)
    
    @property
    def left(self):
        return Point(self._center.x - self._width / 2, self._center.y)
    
    @property
    def right(self):
        return Point(self._center.x + self._width / 2, self._center.y)
    
    @property
    def top_left(self):
        return Point(self._center.x - self._width / 2, self._center.y + self._height / 2)
    
    @property
    def top_right(self):
        return Point(self._center.x + self._width / 2, self._center.y + self._height / 2)
    
    @property
    def bottom_left(self):
        return Point(self._center.x - self._width / 2, self._center.y - self._height / 2)
    
    @property
    def bottom_right(self):
        return Point(self._center.x + self._width / 2, self._center.y - self._height / 2)
    
    # 특정 좌표에서의 점 반환
    def left_at(self, y):
        """왼쪽 면의 특정 y 좌표"""
        return Point(self._center.x - self._width / 2, y)
    
    def right_at(self, y):
        """오른쪽 면의 특정 y 좌표"""
        return Point(self._center.x + self._width / 2, y)
    
    def top_at(self, x):
        """윗면의 특정 x 좌표"""
        return Point(x, self._center.y + self._height / 2)
    
    def bottom_at(self, x):
        """아랫면의 특정 x 좌표"""
        return Point(x, self._center.y - self._height / 2)


# ============================================
# Box (사각형 물체)
# ============================================
class Box(PhysicsObject):
    """사각형 물체 - 2D 변환 행렬 기반"""

    def __init__(self, ax, x=0, y=0, size=(1, 1), on=None, t=0.5,
                 color='lightgray', edgecolor='black', label='',
                 alpha=1.0, lw=1.5, fontsize=12, zorder=5, angle=0):
        super().__init__(ax)

        self._width, self._height = size
        self._rotation = angle  # 추가 회전 각도 (도)

        # on 파라미터 처리: 통일된 Surface 인터페이스 사용
        if on is not None and hasattr(on, 'get_surface_transform'):
            # 표면의 로컬 좌표계 획득
            transform = on.get_surface_transform(t)

            # 로컬 좌표에서 박스 중심 위치:
            # - x' = 0 (표면 위)
            # - y' = height/2 (밑면이 표면에 밀착)
            local_center = Point(0, self._height / 2)

            # 월드 좌표로 변환
            self._center = transform.local_to_world(local_center)

            # 박스 회전 각도 = 표면 각도 + 추가 각도
            self._rotation = transform.angle_deg + angle

            # 변환 정보 저장
            self._surface_transform = transform
        else:
            # on이 없거나 Surface가 아닌 경우
            self._center = Point(x, y)
            self._surface_transform = Transform2D(
                origin=(x, y - self._height / 2),
                angle_rad=np.radians(angle)
            )

        # 꼭짓점 계산 및 그리기
        self._compute_corners()
        self._draw_polygon(ax, color, edgecolor, lw, alpha, zorder)

        # 라벨
        if label:
            ax.text(self._center.x, self._center.y, label,
                    fontsize=fontsize, ha='center', va='center',
                    rotation=self._rotation, zorder=zorder+1)

    def _compute_corners(self):
        """회전된 꼭짓점 계산"""
        hw, hh = self._width / 2, self._height / 2

        # 로컬 좌표계 꼭짓점 (중심 기준)
        local_corners = [
            Point(-hw, -hh),  # bottom-left
            Point(hw, -hh),   # bottom-right
            Point(hw, hh),    # top-right
            Point(-hw, hh),   # top-left
        ]

        # 박스 자체의 변환 행렬 (중심 기준)
        box_transform = Transform2D(
            origin=self._center,
            angle_rad=np.radians(self._rotation)
        )

        # 월드 좌표로 변환
        self._corners = [
            box_transform.local_to_world(corner)
            for corner in local_corners
        ]

    def _draw_polygon(self, ax, color, edgecolor, lw, alpha, zorder):
        """Polygon으로 그리기"""
        polygon = patches.Polygon(
            [(c.x, c.y) for c in self._corners],
            facecolor=color, edgecolor=edgecolor,
            lw=lw, alpha=alpha, zorder=zorder, closed=True
        )
        ax.add_patch(polygon)

    # 회전 고려 프로퍼티들
    @property
    def corners(self):
        """4개의 꼭짓점 [bottom-left, bottom-right, top-right, top-left]"""
        return self._corners

    @property
    def bottom_left(self):
        return self._corners[0]

    @property
    def bottom_right(self):
        return self._corners[1]

    @property
    def top_right(self):
        return self._corners[2]

    @property
    def top_left(self):
        return self._corners[3]

    @property
    def top(self):
        """윗면의 중점"""
        return (self._corners[2] + self._corners[3]) / 2

    @property
    def bottom(self):
        """아랫면의 중점"""
        return (self._corners[0] + self._corners[1]) / 2

    @property
    def left(self):
        """왼쪽 면의 중점"""
        return (self._corners[0] + self._corners[3]) / 2

    @property
    def right(self):
        """오른쪽 면의 중점"""
        return (self._corners[1] + self._corners[2]) / 2

    @property
    def rotation(self):
        """회전 각도 (도)"""
        return self._rotation

    @property
    def surface_normal(self):
        """표면의 법선 방향 단위 벡터"""
        return self._surface_transform.normal

    @property
    def surface_tangent(self):
        """표면의 접선 방향 단위 벡터"""
        return self._surface_transform.tangent

# ============================================
# MassPoint (질점)
# ============================================
class MassPoint(PhysicsObject):
    """질점 (검은 점)"""
    
    def __init__(self, ax, x=0, y=0, on=None,
                 size=12, color='black', zorder=10):
        super().__init__(ax)
        
        # on 파라미터 처리
        if on is not None:
            if hasattr(on, 'center'):
                x, y = on.center.x, on.center.y
            elif hasattr(on, 'top'):
                y = on.top.y
        
        self._center = Point(x, y)
        self._width = 0
        self._height = 0
        
        ax.plot(x, y, 'o', color=color, markersize=size, zorder=zorder)


# ============================================
# Circle (원형 물체)
# ============================================
class Circle(PhysicsObject):
    """원형 물체 - 2D 변환 행렬 기반"""

    def __init__(self, ax, x=0, y=0, radius=0.5, on=None, t=0.5,
                 color='lightblue', edgecolor='black', label='',
                 lw=1.5, alpha=1.0, fontsize=12, zorder=5):
        super().__init__(ax)

        self._width = radius * 2
        self._height = radius * 2
        self._radius = radius

        # on 파라미터 처리: 통일된 Surface 인터페이스 사용
        if on is not None and hasattr(on, 'get_surface_transform'):
            transform = on.get_surface_transform(t)

            # 로컬 좌표에서 원 중심 위치: (0, radius)
            local_center = Point(0, radius)
            self._center = transform.local_to_world(local_center)

            # 변환 정보 저장
            self._surface_transform = transform
        else:
            self._center = Point(x, y)
            self._surface_transform = Transform2D(
                origin=(x, y - radius),
                angle_rad=0
            )

        # 그리기
        circle = patches.Circle(
            (self._center.x, self._center.y), radius,
            facecolor=color, edgecolor=edgecolor,
            lw=lw, alpha=alpha, zorder=zorder
        )
        ax.add_patch(circle)

        if label:
            ax.text(self._center.x, self._center.y, label,
                    fontsize=fontsize, ha='center', va='center',
                    zorder=zorder+1)

    @property
    def radius(self):
        return self._radius

    @property
    def bottom(self):
        """바닥 접점 (표면 법선 방향 기준)"""
        return self._center - self._surface_transform.normal * self._radius

    @property
    def top(self):
        """꼭대기 점"""
        return self._center + self._surface_transform.normal * self._radius

    @property
    def surface_normal(self):
        """표면의 법선 방향 단위 벡터"""
        return self._surface_transform.normal

    @property
    def surface_tangent(self):
        """표면의 접선 방향 단위 벡터"""
        return self._surface_transform.tangent


# ============================================
# Ground (바닥)
# ============================================
class Ground(PhysicsObject):
    """바닥 + 빗금"""
    
    def __init__(self, ax, y=0, xlim=(-2, 8), depth=0.5,
                 color='#d4a574', hatch_spacing=1, alpha=0.7):
        super().__init__(ax)
        
        x_min, x_max = xlim
        self._center = Point((x_min + x_max) / 2, y - depth / 2)
        self._width = x_max - x_min
        self._height = depth
        self._top_y = y
        
        # 바닥 채우기
        ax.fill_between([x_min, x_max], [y - depth, y - depth], [y, y],
                        color=color, alpha=alpha)
        
        # 바닥 선
        ax.plot([x_min, x_max], [y, y], 'k-', lw=1.5)
        
        # 빗금
        for i in np.arange(x_min, x_max, hatch_spacing):
            ax.plot([i, i + 0.5], [y, y - depth], 'k-', lw=0.5)
    
    @property
    def top(self):
        return Point(self._center.x, self._top_y)

    def get_surface_transform(self, t=0.5):
        """표면 위 t 위치의 로컬 좌표계 반환 (수평)"""
        x_min = self._center.x - self._width / 2
        surface_x = x_min + t * self._width
        return Transform2D(origin=(surface_x, self._top_y), angle_rad=0)


# ============================================
# Incline (경사면)
# ============================================
class Incline(PhysicsObject):
    """경사면
    
    Args:
        direction: '+' (／ 모양) or '-' (＼ 모양)
        width, height: 경사면의 가로, 세로 크기
        angle_offset: 각도 라벨 위치 조절 (x, y)
    """
    
    def __init__(self, ax, origin=(0, 0), width = None, height = None, direction='+',
                 color='#d4a574', alpha=0.5, show_angle=True,
                 angle_offset=(0, 0), angle_radius=2, angle = None):
        super().__init__(ax)
        
        self._origin = Point(origin)
        self._direction = direction
        
        if width and height and angle is None:
            self._width = width
            self._height = height
            self._angle = np.arctan2(height, width)  # 라디안으로 통일
    
        elif width and angle and height is None:
            self._width = width
            self._height = width * np.tan(np.radians(angle))
            self._angle = np.radians(angle)
    
        elif height and angle and width is None:
            self._width = height / np.tan(np.radians(angle))
            self._height = height
            self._angle = np.radians(angle)

        else:
            raise ValueError("width+height 또는 width+angle 또는 height+angle 조합 필요")

        ox, oy = origin
        
        if direction == '-':  # ／ 모양 (왼쪽 위 → 오른쪽 아래)
            # 꼭짓점: 왼쪽위, 오른쪽아래, 왼쪽아래
            incline_x = [ox, ox + self._width, ox, ox]
            incline_y = [oy + self._height, oy, oy, oy + self._height]
            
            # 경사면 선
            slope_start = Point(ox, oy + self._height)
            slope_end = Point(ox + self._width, oy)
            
            # 각도 표시 위치 (오른쪽 아래 모서리)
            angle_center = (ox + width, oy)
            theta1 = 180 - np.degrees(self._angle)
            theta2 = 180
            
        else:  # 'left' - ＼ 모양 (오른쪽 위 → 왼쪽 아래)
            # 꼭짓점: 오른쪽위, 왼쪽아래, 오른쪽아래
            incline_x = [ox + self._width, ox, ox + self._width, ox + self._width]
            incline_y = [oy + self._height, oy, oy, oy + self._height]
            
            # 경사면 선
            slope_start = Point(ox + self._width, oy + self._height)
            slope_end = Point(ox, oy)
            
            # 각도 표시 위치 (왼쪽 아래 모서리)
            angle_center = (ox, oy)
            theta1 = 0
            theta2 = np.degrees(self._angle)
        
        self._slope_start = slope_start
        self._slope_end = slope_end
        
        # 그리기
        ax.fill(incline_x, incline_y, color=color, alpha=alpha)
        ax.plot([ox, ox + self._width], [oy, oy], 'k-', lw=1.5)  # 바닥
        
        if direction == '-':
            ax.plot([ox, ox], [oy, oy + self._height], 'k-', lw=1.5)  # 왼쪽 벽
        else:
            ax.plot([ox + self._width, ox + self._width], [oy, oy + self._height], 'k-', lw=1.5)  # 오른쪽 벽
            
        ax.plot([slope_start.x, slope_end.x], [slope_start.y, slope_end.y], 'k-', lw=1.5)  # 경사면
        
        # 각도 표시
        if show_angle:
            arc = patches.Arc(
                angle_center, angle_radius, angle_radius,
                angle=0, theta1=theta1, theta2=theta2,
                color='black', lw=1.5
            )
            ax.add_patch(arc)
            
            # 각도 라벨
            mid_angle = np.radians((theta1 + theta2) / 2)
            label_x = angle_center[0] + (angle_radius/2 + 0.3) * np.cos(mid_angle) + angle_offset[0]
            label_y = angle_center[1] + (angle_radius/2 + 0.3) * np.sin(mid_angle) + angle_offset[1]
            ax.text(label_x, label_y, r'$\theta$', fontsize=14, color='black')
        
        self._center = Point(ox + self._width/2, oy + self._height/2)
    
    def point_on_surface(self, t):
        """경사면 위의 점 (t: 0~1, t=0은 항상 왼쪽)"""
        # '+' 방향일 때 t 반전 (왼쪽 기준 통일)
        adjusted_t = 1 - t if self._direction == '+' else t
        
        return Point(
            self._slope_start.x + adjusted_t * (self._slope_end.x - self._slope_start.x),
            self._slope_start.y + adjusted_t * (self._slope_end.y - self._slope_start.y)
        )
    
    @property
    def slope_start(self):
        """경사면 시작점 (높은 쪽)"""
        return self._slope_start
    
    @property
    def slope_end(self):
        """경사면 끝점 (낮은 쪽)"""
        return self._slope_end
    
    @property
    def angle_rad(self):
        return self._angle
    
    @property
    def angle_deg(self):
        return np.degrees(self._angle)

    def get_surface_transform(self, t=0.5):
        """경사면 위 t 위치의 로컬 좌표계 반환

        Args:
            t: 0~1, 왼쪽에서 오른쪽 방향

        Returns:
            Transform2D: x'축이 경사면 따라 오른쪽, y'축이 법선 방향(위쪽)
        """
        # 경사면 위의 점 계산
        surface_point = self.point_on_surface(t)

        # 경사면 각도 (오른쪽 방향 기준)
        if self._direction == '-':  # ／ 모양: 오른쪽으로 갈수록 낮아짐
            surface_angle = -self._angle
        else:  # '+' ＼ 모양: 오른쪽으로 갈수록 높아짐
            surface_angle = self._angle

        return Transform2D(origin=surface_point, angle_rad=surface_angle)


# ============================================
# Ceiling (천장)
# ============================================
class Ceiling(PhysicsObject):
    """천장 + 빗금"""
    
    def __init__(self, ax, y=2, xlim=(-2, 2), depth=0.3):
        super().__init__(ax)
        
        x_min, x_max = xlim
        self._center = Point((x_min + x_max) / 2, y + depth / 2)
        self._width = x_max - x_min
        self._height = depth
        self._bottom_y = y
        
        # 천장 선
        ax.plot([x_min, x_max], [y, y], 'k-', lw=3)
        
        # 빗금
        for i in np.arange(x_min, x_max, 0.3):
            ax.plot([i, i + 0.3], [y, y + depth], 'k-', lw=1)
    
    @property
    def bottom(self):
        return Point(self._center.x, self._bottom_y)


# ============================================
# Pulley (도르래)
# ============================================
class Pulley(PhysicsObject):
    """도르래"""
    
    def __init__(self, ax, x=0, y=0, radius=0.25,
                 color='white', edgecolor='black', lw=1.5, zorder=10):
        super().__init__(ax)
        
        self._center = Point(x, y)
        self._radius = radius
        self._width = radius * 2
        self._height = radius * 2
        self._right = Point(x + radius, y)
        self._left = Point(x - radius, y)

        circle_out = patches.Circle(
            (x, y), radius,
            facecolor=color, edgecolor=edgecolor, lw=lw, zorder=zorder
        )
        circle_in = patches.Circle(
            (x, y), radius * 0.7,
            facecolor=color, edgecolor=edgecolor, lw=lw, zorder=zorder
        )
        ax.add_patch(circle_out)
        ax.add_patch(circle_in)


# ============================================
# Rope (줄/밧줄)
# ============================================
class Rope:
    """줄/밧줄 연결
    
    Args:
        horizontal: True면 start의 y좌표로 수평 연결
        vertical: True면 start의 x좌표로 수직 연결
    """
    
    def __init__(self, ax, start, end, width=0.08,
                 color='#8B4513', show_texture=True, lw=1.5,
                 horizontal=False, vertical=False):
        
        start = Point(start)
        end = Point(end)
        
        # 수평/수직 강제
        if horizontal:
            end = Point(end.x, start.y)
        if vertical:
            end = Point(start.x, end.y)
        
        # 수직인지 확인
        if abs(start.x - end.x) < 0.01:  # 수직
            ax.fill_betweenx(
                [min(start.y, end.y), max(start.y, end.y)],
                start.x - width, start.x + width,
                color=color, alpha=0.8
            )
            
            # 꼬임 표현
            if show_texture:
                for y in np.arange(min(start.y, end.y), max(start.y, end.y), 0.15):
                    ax.plot([start.x - width, start.x + width], 
                            [y, y + 0.1], color='#5D3A1A', lw=1)
            
            # 테두리
            ax.plot([start.x - width, start.x - width], 
                    [start.y, end.y], color='#5D3A1A', lw=1)
            ax.plot([start.x + width, start.x + width], 
                    [start.y, end.y], color='#5D3A1A', lw=1)
        else:
            # 일반 선
            ax.plot([start.x, end.x], [start.y, end.y], 
                    color=color, lw=lw)


# ============================================
# Table (테이블)
# ============================================
class Table(PhysicsObject):
    """테이블/책상"""
    
    def __init__(self, ax, x=0, y=0, width=4, height=0.2,
                 color='#d4a574', edgecolor='black', alpha=0.7):
        super().__init__(ax)
        
        self._center = Point(x + width/2, y + height/2)
        self._width = width
        self._height = height
        self._top_y = y + height
        
        # 테이블 상판
        ax.fill_between(
            [x, x + width], 
            [y, y],[y + height, y + height],
            color=color, alpha=alpha
        )

    
    @property
    def top(self):
        return Point(self._center.x, self._top_y)

    def get_surface_transform(self, t=0.5):
        """표면 위 t 위치의 로컬 좌표계 반환 (수평)"""
        x_start = self._center.x - self._width / 2
        surface_x = x_start + t * self._width
        return Transform2D(origin=(surface_x, self._top_y), angle_rad=0)


# ============================================
# 화살표 함수 (벡터)
# ============================================
def arrow(ax, start, end, color, label='', label_offset=(0.3, 0),
          fontsize=12, lw=2, zorder=10):
    """화살표(벡터) 그리기"""
    
    start = Point(start)
    end = Point(end)
    
    ax.annotate('', xy=end.tuple, xytext=start.tuple,
                arrowprops=dict(arrowstyle='->', color=color, lw=lw),
                zorder=zorder)
    
    if label:
        mid = Point((start.x + end.x) / 2 + label_offset[0],
                    (start.y + end.y) / 2 + label_offset[1])
        ax.text(mid.x, mid.y, label, fontsize=fontsize, color=color,
                fontweight='bold', ha='center', va='center', zorder=zorder+1)


# ============================================
# 각도 호
# ============================================
def angle_arc(ax, center, radius, theta1, theta2, 
              color=ORANGE, lw=1.5, label='', label_offset=0.3):
    """각도 호 그리기"""
    
    center = Point(center)
    
    arc = patches.Arc(
        center.tuple, radius * 2, radius * 2,
        angle=0, theta1=theta1, theta2=theta2,
        color=color, lw=lw, linestyle='--'
    )
    ax.add_patch(arc)
    
    if label:
        mid_angle = np.radians((theta1 + theta2) / 2)
        label_pos = center + (
            (radius + label_offset) * np.cos(mid_angle),
            (radius + label_offset) * np.sin(mid_angle)
        )
        ax.text(label_pos.x, label_pos.y, label,
                fontsize=14, color=color, ha='center', va='center')


# ============================================
# 좌표축
# ============================================
def coord_axes(ax, origin, length=1.5, angle=0,
               labels=("x'", "y'"), color=GRAY, fontsize=11):
    """좌표축 그리기 (회전 가능)"""
    
    origin = Point(origin)
    theta = np.radians(angle)
    
    # x축
    x_end = origin + (length * np.cos(theta), -length * np.sin(theta))
    ax.annotate('', xy=x_end.tuple, xytext=origin.tuple,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    ax.text(x_end.x + 0.2, x_end.y, labels[0], fontsize=fontsize, color=color)
    
    # y축
    y_end = origin + (length * np.sin(theta), length * np.cos(theta))
    ax.annotate('', xy=y_end.tuple, xytext=origin.tuple,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    ax.text(y_end.x, y_end.y + 0.2, labels[1], fontsize=fontsize, color=color)


# ============================================
# 수식 박스
# ============================================
def formula_box(ax, x, y, text, fontsize=13,
                boxcolor='lightyellow', alpha=0.8):
    """수식 박스"""
    ax.text(x, y, text, fontsize=fontsize, ha='center',
            bbox=dict(boxstyle='round', facecolor=boxcolor, alpha=alpha))


# ============================================
# 토크 방향 표시 (⊙ 또는 ⊗)
# ============================================
class TorqueSymbol(PhysicsObject):
    """토크 방향 기호 (⊙: 나오는 방향, ⊗: 들어가는 방향)"""
    
    def __init__(self, ax, x=0, y=0, radius=0.25, direction='out',
                 color=PURPLE, lw=3, zorder=10):
        super().__init__(ax)
        
        self._center = Point(x, y)
        self._width = radius * 2
        self._height = radius * 2
        
        # 원
        circle = patches.Circle(
            (x, y), radius,
            fill=False, color=color, lw=lw, zorder=zorder
        )
        ax.add_patch(circle)
        
        if direction == 'out':  # ⊙
            ax.plot(x, y, 'o', color=color, markersize=6, zorder=zorder+1)
        else:  # ⊗
            d = radius * 0.6
            ax.plot([x - d, x + d], [y - d, y + d], color=color, lw=lw, zorder=zorder+1)
            ax.plot([x - d, x + d], [y + d, y - d], color=color, lw=lw, zorder=zorder+1)