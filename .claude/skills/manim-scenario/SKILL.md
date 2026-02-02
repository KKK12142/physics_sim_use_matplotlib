---
name: manim-scenario
description: Design storyboards and scenarios for Manim physics animations in YAML format. Use when planning animation sequences, defining objects, timelines, camera movements, or preparing content before using manim-physics skill. Outputs structured YAML for physics education videos.
---

# Manim Scenario Designer

Design structured storyboards for physics education animations before coding with Manim.

## Quick start

```yaml
scene:
  name: "Newton Second Law"
  standard: "[12물리01-02]"
  duration: 8s

objects:
  - id: box
    type: square
    color: BLUE
    size: 1
    position: [-4, 0]

  - id: force
    type: arrow
    color: RED
    from: box.left
    direction: [1, 0]
    label: "\\vec{F}"

equations:
  - id: eq1
    latex: "F = ma"
    position: UR

timeline:
  - at: 0s
    action: create
    target: box

  - at: 1s
    action: create
    target: [force, eq1]

  - at: 2s
    action: move
    target: box
    to: [3, 0]
    duration: 3s
    easing: ease_in_quad
```

## Instructions

1. **Define scene metadata**: name, curriculum standard, total duration

2. **List all objects** with properties:
   - Shapes: square, circle, polygon, line
   - Vectors: arrow with from/to or direction
   - Text/Math: label, equation
   - Graphs: axes with plots

3. **Write timeline** in chronological order:
   - Each entry has `at` (timestamp) and `action`
   - Actions: create, move, transform, fade_in, fade_out, rotate
   - Use `target` for single object, `targets` for multiple

4. **Add camera directions** if needed:
   - zoom, pan, follow, reset

5. **Specify graphs** if showing data:
   - Link to object motion for real-time sync

## Object types

### Physical objects

```yaml
objects:
  - id: ball
    type: circle
    radius: 0.3
    color: RED
    fill_opacity: 0.8
    position: [0, 2]
    
  - id: ground
    type: line
    from: [-5, -2]
    to: [5, -2]
    color: WHITE
    
  - id: incline
    type: polygon
    vertices: [[0, 0], [4, 0], [4, 2]]
    color: GRAY
    fill_opacity: 0.5
```

### Vectors

```yaml
objects:
  - id: velocity
    type: arrow
    color: BLUE
    from: ball.center
    direction: [2, 0]
    label: "\\vec{v}"
    label_position: UP
    
  - id: force_components
    type: arrow_group
    arrows:
      - direction: [1, 0]
        color: RED
        label: "F_x"
      - direction: [0, -1]
        color: RED
        label: "F_y"
```

### Equations and text

```yaml
equations:
  - id: newton
    latex: "\\vec{F} = m\\vec{a}"
    position: UR
    font_size: 36
    
  - id: label
    text: "Initial position"
    position: object.ball.below
    font_size: 24
```

### Graphs

```yaml
graphs:
  - id: vt_graph
    type: axes
    position: [4, 0]
    size: [3, 2]
    x_range: [0, 5]
    y_range: [0, 10]
    x_label: "t"
    y_label: "v"
    plots:
      - function: "2 + 1.5*t"
        color: BLUE
        sync_with: ball.velocity.magnitude
```

## Timeline actions

### Basic actions

```yaml
timeline:
  - at: 0s
    action: create
    target: box
    animation: fade_in  # or grow_from_center, draw
    
  - at: 1s
    action: move
    target: box
    to: [3, 0]
    duration: 2s
    easing: linear  # ease_in, ease_out, ease_in_out
    
  - at: 3s
    action: rotate
    target: arrow
    angle: 45  # degrees
    duration: 1s
    
  - at: 4s
    action: transform
    target: eq1
    to_latex: "a = \\frac{F}{m}"
    duration: 0.5s
    
  - at: 5s
    action: fade_out
    targets: [box, arrow]
```

### Simultaneous actions

```yaml
timeline:
  - at: 2s
    actions:
      - action: move
        target: box
        to: [3, 0]
      - action: update
        target: vt_graph
        trace: true
```

## Camera

```yaml
camera:
  - at: 3s
    action: zoom
    scale: 2
    focus: box
    duration: 1s
    
  - at: 5s
    action: pan
    to: [4, 0]
    duration: 1s
    
  - at: 7s
    action: follow
    target: ball
    duration: 3s
```

## Color conventions

| Physical quantity | Color | Manim constant |
|------------------|-------|----------------|
| Force | Red | RED |
| Velocity | Blue | BLUE |
| Acceleration | Orange | ORANGE |
| Displacement | Green | GREEN |
| Energy | Yellow-Green | YELLOW_GREEN |
| Electric field | Yellow | YELLOW |
| Magnetic field | Purple | PURPLE |
| Positive charge | Red | RED |
| Negative charge | Blue | BLUE |

## Position shortcuts

| Code | Meaning |
|------|---------|
| UL, UR, DL, DR | Corners (Up-Left, etc.) |
| UP, DOWN, LEFT, RIGHT | Edges |
| ORIGIN | Center [0, 0] |
| object.id.center | Object center |
| object.id.left/right/up/down | Object edges |
| object.id.above/below | Relative to object |

## Best practices

- Start with scene metadata and curriculum standard
- Define all objects before writing timeline
- Use descriptive IDs (force_gravity, not f1)
- Keep individual animations under 3 seconds
- Add wait time between major concepts
- Group related objects for simultaneous actions
- Include equations alongside visualizations

## Requirements

This skill outputs YAML scenarios. Use with manim-physics skill for implementation.

## Templates

For curriculum-specific templates, see [references/templates.md](references/templates.md)

For complete YAML schema, see [references/schema.md](references/schema.md)
