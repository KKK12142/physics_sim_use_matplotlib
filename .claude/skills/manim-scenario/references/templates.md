# Physics Scenario Templates

Templates organized by Korean 2022 Revised Physics Curriculum standards.

## Mechanics (힘과 에너지)

### [12물리01-01] Force Equilibrium

```yaml
scene:
  name: "Force Equilibrium"
  standard: "[12물리01-01]"
  duration: 12s
  description: "Forces in equilibrium and torque balance"

objects:
  - id: box
    type: square
    size: 1.2
    color: BLUE
    fill_opacity: 0.6
    position: [0, 0]

  - id: f1
    type: arrow
    color: RED
    from: box.center
    direction: [2, 0]
    label: "\\vec{F}_1"

  - id: f2
    type: arrow
    color: RED
    from: box.center
    direction: [-2, 0]
    label: "\\vec{F}_2"

  - id: f3
    type: arrow
    color: RED
    from: box.center
    direction: [0, 1.5]
    label: "\\vec{F}_3"

  - id: f4
    type: arrow
    color: RED
    from: box.center
    direction: [0, -1.5]
    label: "\\vec{F}_4"

equations:
  - id: equilibrium
    latex: "\\sum \\vec{F} = 0"
    position: UR

  - id: components
    latex: "\\sum F_x = 0, \\quad \\sum F_y = 0"
    position: DR

timeline:
  - at: 0s
    action: create
    target: box

  - at: 1s
    action: create
    targets: [f1, f2]

  - at: 2s
    action: create
    targets: [f3, f4]

  - at: 3s
    action: create
    target: equilibrium

  - at: 5s
    action: create
    target: components

  - at: 7s
    action: wait
    duration: 3s
    note: "Show that box remains stationary"
```

### [12물리01-02] Newton's Second Law

```yaml
scene:
  name: "Newton Second Law"
  standard: "[12물리01-02]"
  duration: 15s
  description: "F=ma with motion graphs"

objects:
  - id: box
    type: square
    size: 1
    color: BLUE
    fill_opacity: 0.6
    position: [-5, 0]

  - id: force
    type: arrow
    color: RED
    from: box.left
    direction: [1.5, 0]
    label: "\\vec{F}"

  - id: accel
    type: arrow
    color: ORANGE
    from: box.right
    direction: [1, 0]
    label: "\\vec{a}"

equations:
  - id: newton
    latex: "\\vec{F} = m\\vec{a}"
    position: UR

  - id: kinematic
    latex: "v = v_0 + at"
    position: UR
    below: newton

graphs:
  - id: vt
    type: axes
    position: [4, 1]
    size: [3, 2]
    x_range: [0, 5]
    y_range: [0, 8]
    x_label: "t (s)"
    y_label: "v (m/s)"
    plots:
      - function: "1.5*t"
        color: BLUE
        label: "v(t)"

  - id: xt
    type: axes
    position: [4, -2]
    size: [3, 2]
    x_range: [0, 5]
    y_range: [0, 20]
    x_label: "t (s)"
    y_label: "x (m)"
    plots:
      - function: "0.75*t^2"
        color: GREEN
        label: "x(t)"

timeline:
  - at: 0s
    action: create
    targets: [box, force, accel]

  - at: 1s
    action: create
    target: newton

  - at: 2s
    action: create
    targets: [vt, xt]

  - at: 3s
    actions:
      - action: move
        target: box
        to: [3, 0]
        duration: 4s
        easing: ease_in_quad
      - action: trace
        target: vt
        sync_with: box.velocity
      - action: trace
        target: xt
        sync_with: box.position
```

### [12물리01-03] Momentum Conservation

```yaml
scene:
  name: "Momentum Conservation - Collision"
  standard: "[12물리01-03]"
  duration: 12s
  description: "Elastic collision between two balls"

objects:
  - id: ball1
    type: circle
    radius: 0.4
    color: RED
    fill_opacity: 0.8
    position: [-4, 0]
    label: "m_1"

  - id: ball2
    type: circle
    radius: 0.5
    color: BLUE
    fill_opacity: 0.8
    position: [1, 0]
    label: "m_2"

  - id: v1_before
    type: arrow
    color: GREEN
    from: ball1.right
    direction: [2, 0]
    label: "v_1"

  - id: v2_before
    type: arrow
    color: GREEN
    from: ball2.left
    direction: [-1, 0]
    label: "v_2"

equations:
  - id: momentum
    latex: "m_1 v_1 + m_2 v_2 = m_1 v_1' + m_2 v_2'"
    position: UP

  - id: energy
    latex: "\\frac{1}{2}m_1 v_1^2 + \\frac{1}{2}m_2 v_2^2 = \\frac{1}{2}m_1 v_1'^2 + \\frac{1}{2}m_2 v_2'^2"
    position: DOWN

timeline:
  - at: 0s
    action: create
    targets: [ball1, ball2]

  - at: 1s
    action: create
    targets: [v1_before, v2_before]

  - at: 2s
    action: create
    target: momentum

  - at: 3s
    actions:
      - action: move
        target: ball1
        to: [-0.5, 0]
        duration: 1.5s
      - action: move
        target: ball2
        to: [0.5, 0]
        duration: 1.5s

  - at: 4.5s
    action: flash
    target: [ball1, ball2]
    note: "Collision moment"

  - at: 5s
    actions:
      - action: move
        target: ball1
        to: [-2, 0]
        duration: 2s
      - action: move
        target: ball2
        to: [4, 0]
        duration: 2s

  - at: 7s
    action: transform
    target: v1_before
    note: "Update velocity arrows to show v1' and v2'"
```

### [12물리01-04] Work-Energy Theorem

```yaml
scene:
  name: "Work-Energy Theorem"
  standard: "[12물리01-04]"
  duration: 15s
  description: "Work done equals change in kinetic energy"

objects:
  - id: box
    type: square
    size: 0.8
    color: BLUE
    position: [-4, 0]

  - id: force
    type: arrow
    color: RED
    from: box.left
    direction: [1.5, 0]
    label: "F"

  - id: displacement
    type: arrow
    color: GREEN
    from: [-4, -1]
    to: [2, -1]
    label: "d"
    style: dashed

equations:
  - id: work
    latex: "W = Fd"
    position: UL

  - id: theorem
    latex: "W = \\Delta KE = \\frac{1}{2}mv_f^2 - \\frac{1}{2}mv_i^2"
    position: UR

graphs:
  - id: energy_bar
    type: bar_chart
    position: [4, 0]
    bars:
      - id: ke
        label: "KE"
        color: ORANGE
        initial_value: 0
      - id: work_done
        label: "W"
        color: YELLOW
        initial_value: 0

timeline:
  - at: 0s
    action: create
    targets: [box, force, displacement]

  - at: 1s
    action: create
    target: work

  - at: 2s
    action: create
    targets: [theorem, energy_bar]

  - at: 3s
    actions:
      - action: move
        target: box
        to: [2, 0]
        duration: 3s
        easing: ease_in_quad
      - action: update
        target: energy_bar.ke
        to_value: 100
        duration: 3s
```

### [12물리01-05] Energy Conservation (Pendulum)

```yaml
scene:
  name: "Pendulum Energy Conservation"
  standard: "[12물리01-05]"
  duration: 20s
  description: "PE and KE exchange in pendulum motion"

objects:
  - id: pivot
    type: dot
    position: [0, 2]
    color: WHITE

  - id: string
    type: line
    from: pivot
    to: bob
    color: WHITE

  - id: bob
    type: circle
    radius: 0.3
    color: RED
    fill_opacity: 0.8
    position: [-2, 0]

  - id: height_line
    type: dashed_line
    from: [-3, 0]
    to: [3, 0]
    color: GRAY
    label: "h = 0"

equations:
  - id: conservation
    latex: "E = KE + PE = const"
    position: UR

  - id: values
    latex: "\\frac{1}{2}mv^2 + mgh = const"
    position: DR

graphs:
  - id: energy_bars
    type: stacked_bar
    position: [4, 0]
    bars:
      - id: pe
        label: "PE"
        color: BLUE
      - id: ke
        label: "KE"
        color: ORANGE

timeline:
  - at: 0s
    action: create
    targets: [pivot, string, bob, height_line]

  - at: 1s
    action: create
    targets: [conservation, energy_bars]

  - at: 2s
    action: pendulum_swing
    target: bob
    pivot: pivot
    amplitude: 60
    periods: 3
    duration: 9s
    sync_energy: energy_bars
```

## Electromagnetism (전기와 자기)

### [12물리02-01] Electric Field

```yaml
scene:
  name: "Electric Field of Point Charges"
  standard: "[12물리02-01]"
  duration: 15s
  description: "Electric field lines from point charges"

objects:
  - id: positive
    type: charge
    sign: positive
    position: [-2, 0]
    color: RED
    label: "+q"

  - id: negative
    type: charge
    sign: negative
    position: [2, 0]
    color: BLUE
    label: "-q"

  - id: field_lines
    type: field_line_set
    source: positive
    sink: negative
    num_lines: 8
    color: YELLOW

  - id: test_charge
    type: charge
    sign: positive
    radius: 0.1
    position: [0, 1]
    color: GREEN

equations:
  - id: coulomb
    latex: "E = k\\frac{q}{r^2}"
    position: UR

  - id: force
    latex: "\\vec{F} = q\\vec{E}"
    position: DR

timeline:
  - at: 0s
    action: create
    targets: [positive, negative]

  - at: 1s
    action: create
    target: coulomb

  - at: 2s
    action: create
    target: field_lines
    animation: grow_from_source
    duration: 2s

  - at: 5s
    action: create
    target: test_charge

  - at: 6s
    action: create
    target: force

  - at: 7s
    action: move_along_field
    target: test_charge
    duration: 3s
```

### [12물리02-02] Circuit Analysis

```yaml
scene:
  name: "Series and Parallel Circuits"
  standard: "[12물리02-02]"
  duration: 18s
  description: "Comparing series and parallel resistor circuits"

objects:
  - id: battery
    type: battery
    voltage: 12
    position: [-3, 0]

  - id: r1
    type: resistor
    resistance: "R_1"
    position: [0, 1]

  - id: r2
    type: resistor
    resistance: "R_2"
    position: [0, -1]

  - id: wire_series
    type: wire_path
    path: [battery.plus, r1.left, r1.right, r2.left, r2.right, battery.minus]
    color: ORANGE

  - id: current_arrow
    type: arrow
    color: YELLOW
    along_path: wire_series
    label: "I"

equations:
  - id: series
    latex: "R_{series} = R_1 + R_2"
    position: UL

  - id: parallel
    latex: "\\frac{1}{R_{parallel}} = \\frac{1}{R_1} + \\frac{1}{R_2}"
    position: UR

  - id: ohm
    latex: "V = IR"
    position: DOWN

timeline:
  - at: 0s
    action: create
    targets: [battery, r1, r2]
    note: "Series configuration"

  - at: 1s
    action: create
    target: wire_series

  - at: 2s
    action: create
    target: series

  - at: 3s
    action: animate_current
    target: current_arrow
    duration: 3s

  - at: 7s
    action: transform
    note: "Reconfigure to parallel"
    targets: [r1, r2, wire_series]
    duration: 2s

  - at: 10s
    action: create
    target: parallel
```

### [12물리02-06] Electromagnetic Induction

```yaml
scene:
  name: "Faraday's Law"
  standard: "[12물리02-06]"
  duration: 15s
  description: "Electromagnetic induction and Lenz's law"

objects:
  - id: coil
    type: coil
    turns: 5
    position: [0, 0]
    color: ORANGE

  - id: magnet
    type: magnet
    north_color: RED
    south_color: BLUE
    position: [-4, 0]
    label_n: "N"
    label_s: "S"

  - id: b_field
    type: field_arrows
    direction: RIGHT
    region: coil.interior
    color: PURPLE

  - id: induced_current
    type: current_indicator
    in_coil: coil
    color: YELLOW

equations:
  - id: faraday
    latex: "\\mathcal{E} = -\\frac{d\\Phi_B}{dt}"
    position: UR

  - id: flux
    latex: "\\Phi_B = BA\\cos\\theta"
    position: DR

graphs:
  - id: flux_graph
    type: axes
    position: [4, 1]
    x_label: "t"
    y_label: "\\Phi_B"

  - id: emf_graph
    type: axes
    position: [4, -1]
    x_label: "t"
    y_label: "\\mathcal{E}"

timeline:
  - at: 0s
    action: create
    targets: [coil, magnet]

  - at: 1s
    action: create
    target: faraday

  - at: 2s
    action: create
    targets: [flux_graph, emf_graph]

  - at: 3s
    actions:
      - action: move
        target: magnet
        to: [-1, 0]
        duration: 3s
      - action: show
        target: b_field
        animation: grow
      - action: trace
        target: flux_graph
      - action: trace
        target: emf_graph

  - at: 7s
    action: show
    target: induced_current
    note: "Show induced current direction (Lenz's law)"
```

## Optics and Modern Physics (빛과 물질)

### [12물리03-01] Wave Interference

```yaml
scene:
  name: "Double Slit Interference"
  standard: "[12물리03-01]"
  duration: 18s
  description: "Young's double slit experiment"

objects:
  - id: source
    type: wave_source
    position: [-5, 0]
    wavelength: 0.5
    color: YELLOW

  - id: barrier
    type: barrier_with_slits
    position: [-2, 0]
    slit_positions: [0.3, -0.3]
    slit_width: 0.1

  - id: screen
    type: line
    from: [4, -3]
    to: [4, 3]
    color: WHITE

  - id: wave1
    type: circular_wave
    source: barrier.slit1
    color: YELLOW
    opacity: 0.5

  - id: wave2
    type: circular_wave
    source: barrier.slit2
    color: YELLOW
    opacity: 0.5

  - id: interference_pattern
    type: intensity_pattern
    on: screen
    maxima_color: YELLOW
    minima_color: BLACK

equations:
  - id: path_diff
    latex: "d\\sin\\theta = m\\lambda"
    position: UR

  - id: constructive
    latex: "m = 0, \\pm 1, \\pm 2, ..."
    position: DR

timeline:
  - at: 0s
    action: create
    targets: [source, barrier, screen]

  - at: 1s
    action: emit_wave
    target: source
    duration: 2s

  - at: 3s
    action: create
    targets: [wave1, wave2]
    animation: propagate
    duration: 3s

  - at: 6s
    action: show
    target: interference_pattern
    animation: fade_in
    duration: 2s

  - at: 8s
    action: create
    target: path_diff

  - at: 10s
    action: highlight
    target: interference_pattern.maxima
    note: "Mark constructive interference points"
```

### [12물리03-03] Photoelectric Effect

```yaml
scene:
  name: "Photoelectric Effect"
  standard: "[12물리03-03]"
  duration: 15s
  description: "Light quanta and electron emission"

objects:
  - id: metal_plate
    type: rectangle
    size: [3, 0.5]
    color: GRAY
    fill_opacity: 0.8
    position: [0, -1]

  - id: photon
    type: wavy_arrow
    color: YELLOW
    from: [-3, 2]
    to: metal_plate.top
    label: "h\\nu"

  - id: electron
    type: circle
    radius: 0.1
    color: BLUE
    position: metal_plate.top

  - id: electron_path
    type: arrow
    color: BLUE
    from: electron
    direction: [1, 2]
    label: "e^-"

equations:
  - id: einstein
    latex: "h\\nu = W + \\frac{1}{2}mv_{max}^2"
    position: UR

  - id: threshold
    latex: "h\\nu_0 = W"
    position: DR

graphs:
  - id: ke_vs_freq
    type: axes
    position: [4, 0]
    x_label: "\\nu"
    y_label: "KE_{max}"
    plots:
      - function: "h*(x - nu_0)"
        color: GREEN
        x_min: "nu_0"

timeline:
  - at: 0s
    action: create
    target: metal_plate

  - at: 1s
    action: create
    target: photon
    animation: move_along_path
    duration: 1s

  - at: 2s
    action: flash
    target: metal_plate.top
    note: "Photon absorbed"

  - at: 2.5s
    action: create
    targets: [electron, electron_path]
    animation: shoot_out

  - at: 4s
    action: create
    target: einstein

  - at: 6s
    action: create
    target: ke_vs_freq

  - at: 8s
    note: "Show multiple photons with different frequencies"
```

### [12물리03-05] Bohr Model

```yaml
scene:
  name: "Bohr Hydrogen Atom"
  standard: "[12물리03-05]"
  duration: 20s
  description: "Energy levels and spectral lines"

objects:
  - id: nucleus
    type: dot
    radius: 0.15
    color: RED
    position: [0, 0]
    label: "p^+"

  - id: orbit1
    type: circle
    radius: 0.8
    color: GRAY
    stroke_width: 1
    label: "n=1"

  - id: orbit2
    type: circle
    radius: 1.4
    color: GRAY
    stroke_width: 1
    label: "n=2"

  - id: orbit3
    type: circle
    radius: 2.0
    color: GRAY
    stroke_width: 1
    label: "n=3"

  - id: electron
    type: dot
    radius: 0.1
    color: BLUE
    position: orbit3.right

  - id: photon_emitted
    type: wavy_arrow
    color: RED
    from: electron
    direction: [2, 1]

equations:
  - id: energy
    latex: "E_n = -\\frac{13.6}{n^2} \\text{ eV}"
    position: UR

  - id: transition
    latex: "\\Delta E = h\\nu"
    position: DR

graphs:
  - id: energy_levels
    type: energy_diagram
    position: [4, 0]
    levels:
      - n: 1
        energy: -13.6
      - n: 2
        energy: -3.4
      - n: 3
        energy: -1.5
      - n: inf
        energy: 0
        label: "ionization"

timeline:
  - at: 0s
    action: create
    targets: [nucleus, orbit1, orbit2, orbit3]

  - at: 2s
    action: create
    target: electron

  - at: 3s
    action: create
    targets: [energy, energy_levels]

  - at: 5s
    action: transition
    target: electron
    from_orbit: orbit3
    to_orbit: orbit2
    emit: photon_emitted
    duration: 1s

  - at: 7s
    action: highlight
    target: energy_levels
    transition: [3, 2]
    photon_color: RED

  - at: 9s
    action: transition
    target: electron
    from_orbit: orbit2
    to_orbit: orbit1
    emit: photon_emitted
    photon_color: BLUE
```

### [12물리03-06] Special Relativity

```yaml
scene:
  name: "Time Dilation"
  standard: "[12물리03-06]"
  duration: 15s
  description: "Time dilation in moving reference frames"

objects:
  - id: rest_clock
    type: clock
    position: [-3, 0]
    radius: 1
    label: "Rest frame"

  - id: moving_clock
    type: clock
    position: [3, 0]
    radius: 1
    label: "Moving frame (v = 0.8c)"

  - id: spaceship
    type: polygon
    vertices: [[0, 0], [1.5, 0], [1.5, 0.5], [0, 0.5]]
    color: GRAY
    position: [2, -2]

  - id: velocity_arrow
    type: arrow
    color: GREEN
    from: spaceship.right
    direction: [1.5, 0]
    label: "v"

equations:
  - id: gamma
    latex: "\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}"
    position: UL

  - id: dilation
    latex: "\\Delta t' = \\gamma \\Delta t"
    position: UR

  - id: gamma_value
    latex: "\\gamma = 1.67 \\text{ (for } v = 0.8c)"
    position: DR

timeline:
  - at: 0s
    action: create
    targets: [rest_clock, moving_clock, spaceship, velocity_arrow]

  - at: 1s
    action: create
    target: gamma

  - at: 2s
    action: create
    target: dilation

  - at: 3s
    actions:
      - action: rotate_hand
        target: rest_clock
        angle: -360
        duration: 6s
      - action: rotate_hand
        target: moving_clock
        angle: -216
        duration: 6s
        note: "Moving clock runs slower by factor of gamma"

  - at: 10s
    action: create
    target: gamma_value

  - at: 11s
    action: highlight
    targets: [rest_clock, moving_clock]
    note: "Compare final positions of clock hands"
```
