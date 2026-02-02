# YAML Schema Reference

Complete schema for manim-scenario YAML files.

## Root Structure

```yaml
scene:           # Required - Scene metadata
objects:         # Required - All visual elements
equations:       # Optional - Mathematical expressions
graphs:          # Optional - Data visualizations
timeline:        # Required - Animation sequence
camera:          # Optional - Camera movements
settings:        # Optional - Global settings
```

## Scene

```yaml
scene:
  name: string           # Required - Scene title
  standard: string       # Curriculum code, e.g., "[12물리01-02]"
  duration: string       # Total duration, e.g., "15s"
  description: string    # Brief description
  background: color      # Background color (default: BLACK)
  frame_rate: number     # FPS (default: 60)
```

## Objects

### Common Properties

All objects share these properties:

```yaml
- id: string            # Required - Unique identifier
  type: string          # Required - Object type
  position: [x, y]      # Position coordinates
  color: color          # Stroke/fill color
  fill_opacity: number  # 0 to 1
  stroke_width: number  # Line thickness
  label: string         # LaTeX or text label
  label_position: pos   # UP, DOWN, LEFT, RIGHT, UL, UR, DL, DR
```

### Shape Types

#### square / rectangle

```yaml
- id: box
  type: square
  size: number           # Side length
  # or
  type: rectangle
  width: number
  height: number
  corner_radius: number  # Rounded corners
```

#### circle / ellipse

```yaml
- id: ball
  type: circle
  radius: number
  # or
  type: ellipse
  width: number
  height: number
```

#### polygon

```yaml
- id: triangle
  type: polygon
  vertices: [[x1,y1], [x2,y2], [x3,y3], ...]
```

#### line / dashed_line

```yaml
- id: axis
  type: line
  from: [x, y] | object.id.anchor
  to: [x, y] | object.id.anchor
  # or
  type: dashed_line
  dash_length: number
  dash_gap: number
```

#### arc

```yaml
- id: angle_arc
  type: arc
  radius: number
  start_angle: number    # Degrees
  end_angle: number
  center: [x, y]
```

### Vector Types

#### arrow

```yaml
- id: force
  type: arrow
  from: [x, y] | object.id.anchor
  to: [x, y]
  # or
  direction: [dx, dy]    # Relative direction
  magnitude: number      # Arrow length
  tip_size: number       # Arrowhead size
  label: string          # LaTeX label
```

#### arrow_group

```yaml
- id: components
  type: arrow_group
  origin: [x, y] | object.id.anchor
  arrows:
    - direction: [dx, dy]
      color: color
      label: string
    - direction: [dx, dy]
      color: color
      label: string
```

#### vector_field

```yaml
- id: e_field
  type: vector_field
  function: [fx, fy]     # Functions of x, y
  x_range: [min, max]
  y_range: [min, max]
  density: number        # Arrows per unit
  color: color | gradient
```

### Physics Objects

#### charge

```yaml
- id: proton
  type: charge
  sign: positive | negative
  magnitude: number      # Charge value
  radius: number
  show_label: boolean    # Show +/- symbol
```

#### magnet

```yaml
- id: bar_magnet
  type: magnet
  orientation: horizontal | vertical
  north_color: color
  south_color: color
  label_n: string
  label_s: string
```

#### resistor / capacitor / battery

```yaml
- id: r1
  type: resistor
  resistance: string     # Label like "R_1" or "10Ω"
  
- id: c1
  type: capacitor
  capacitance: string
  
- id: v1
  type: battery
  voltage: string
  orientation: horizontal | vertical
```

#### coil

```yaml
- id: solenoid
  type: coil
  turns: number
  width: number
  height: number
  orientation: horizontal | vertical
```

#### wave_source

```yaml
- id: light
  type: wave_source
  wavelength: number
  amplitude: number
  frequency: number
  direction: [dx, dy]
```

### Special Objects

#### field_lines

```yaml
- id: field
  type: field_lines
  source: object.id      # Positive charge / north pole
  sink: object.id        # Negative charge / south pole (optional)
  num_lines: number
  style: curved | straight
```

#### clock

```yaml
- id: timer
  type: clock
  radius: number
  show_numbers: boolean
  hand_lengths: [hour, minute, second]
```

## Equations

```yaml
equations:
  - id: string           # Required
    latex: string        # LaTeX code
    text: string         # Plain text (alternative to latex)
    position: pos        # UL, UR, DL, DR, UP, DOWN, or [x, y]
    font_size: number    # Default: 36
    color: color
    below: equation.id   # Position below another equation
    box: boolean         # Draw box around equation
```

## Graphs

### Axes

```yaml
graphs:
  - id: string           # Required
    type: axes
    position: [x, y]
    size: [width, height]
    x_range: [min, max, step]
    y_range: [min, max, step]
    x_label: string
    y_label: string
    show_grid: boolean
    axis_color: color
    
    plots:               # Functions to plot
      - function: string # e.g., "2*x + 1", "sin(x)"
        color: color
        label: string
        x_range: [min, max]  # Override axis range
        style: solid | dashed | dotted
```

### Bar Chart

```yaml
graphs:
  - id: energy_bars
    type: bar_chart
    position: [x, y]
    size: [width, height]
    bars:
      - id: ke
        label: "KE"
        color: color
        initial_value: number
      - id: pe
        label: "PE"
        color: color
        initial_value: number
```

### Energy Diagram

```yaml
graphs:
  - id: levels
    type: energy_diagram
    position: [x, y]
    levels:
      - n: 1
        energy: -13.6
        label: "n=1"
      - n: 2
        energy: -3.4
```

## Timeline

### Basic Actions

```yaml
timeline:
  - at: time             # Required - "0s", "1.5s", etc.
    action: string       # Required - Action type
    target: id           # Single object
    targets: [id1, id2]  # Multiple objects
    duration: time       # Animation duration
    animation: type      # Animation style
```

### Action Types

#### create

```yaml
- at: 0s
  action: create
  target: box
  animation: fade_in | grow | draw | write
  duration: 1s
```

#### move

```yaml
- at: 1s
  action: move
  target: box
  to: [x, y]
  path: straight | arc | bezier
  duration: 2s
  easing: linear | ease_in | ease_out | ease_in_out | ease_in_quad
```

#### rotate

```yaml
- at: 2s
  action: rotate
  target: arrow
  angle: 90              # Degrees (positive = counterclockwise)
  about: [x, y] | object.id.anchor  # Rotation center
  duration: 1s
```

#### transform

```yaml
- at: 3s
  action: transform
  target: eq1
  to_latex: "new equation"
  duration: 0.5s
```

#### scale

```yaml
- at: 4s
  action: scale
  target: box
  factor: 2              # Scale multiplier
  duration: 1s
```

#### fade_in / fade_out

```yaml
- at: 5s
  action: fade_out
  targets: [box, arrow]
  duration: 0.5s
```

#### flash

```yaml
- at: 6s
  action: flash
  target: collision_point
  color: WHITE
  duration: 0.3s
```

#### trace

```yaml
- at: 7s
  action: trace
  target: graph
  sync_with: object.property  # e.g., ball.velocity
  duration: 5s
```

#### update

```yaml
- at: 8s
  action: update
  target: energy_bars.ke
  to_value: 100
  duration: 2s
```

#### wait

```yaml
- at: 9s
  action: wait
  duration: 2s
  note: "Pause for explanation"
```

### Simultaneous Actions

```yaml
- at: 2s
  actions:
    - action: move
      target: ball
      to: [3, 0]
      duration: 2s
    - action: trace
      target: graph
      duration: 2s
    - action: update
      target: ke_bar
      to_value: 50
```

## Camera

```yaml
camera:
  - at: time
    action: zoom
    scale: number        # 2 = 2x zoom in, 0.5 = zoom out
    focus: [x, y] | object.id
    duration: time
    
  - at: time
    action: pan
    to: [x, y]
    duration: time
    
  - at: time
    action: follow
    target: object.id
    duration: time
    
  - at: time
    action: reset
    duration: time
```

## Settings

```yaml
settings:
  coordinate_system:
    type: cartesian | polar
    origin: [x, y]
    scale: number        # Pixels per unit
    show_axes: boolean
    show_grid: boolean
    
  color_scheme:
    force: RED
    velocity: BLUE
    acceleration: ORANGE
    energy: GREEN
    
  defaults:
    animation_duration: 1s
    font_size: 36
    stroke_width: 2
```

## Color Values

Supported color names:

```
WHITE, BLACK, GRAY, DARK_GRAY, LIGHT_GRAY
RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, PINK
TEAL, GOLD, MAROON, NAVY
RED_A, RED_B, RED_C, RED_D, RED_E (color variants)
BLUE_A through BLUE_E
GREEN_A through GREEN_E
```

## Position Anchors

Object anchors:

```
object.id.center
object.id.left, .right, .up, .down
object.id.ul, .ur, .dl, .dr (corners)
object.id.top, .bottom
object.id.above, .below (with spacing)
```

Screen positions:

```
ORIGIN = [0, 0]
UP, DOWN, LEFT, RIGHT
UL, UR, DL, DR (corners)
```
