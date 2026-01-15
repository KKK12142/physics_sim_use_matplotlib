# 물리 시뮬레이션 템플릿 라이브러리

## 역학 (Mechanics)

### 1. 등속/등가속 운동

#### template-1d-motion.jsx
```jsx
/**
 * 1차원 운동 시뮬레이션
 * - 등속 운동
 * - 등가속도 운동
 * - x-t, v-t, a-t 그래프 동기화
 */

// 조작 변수
const params = {
  initialPosition: 0,      // 초기 위치 (m)
  initialVelocity: 5,      // 초기 속도 (m/s)
  acceleration: 0,         // 가속도 (m/s²)
  timeScale: 1,           // 시간 배율
};

// 물리 계산
function calculateMotion(t) {
  const x = params.initialPosition + 
            params.initialVelocity * t + 
            0.5 * params.acceleration * t * t;
  const v = params.initialVelocity + params.acceleration * t;
  return { x, v, a: params.acceleration };
}
```

### 2. 포물선 운동

#### template-projectile.jsx
```jsx
/**
 * 포물선 운동 시뮬레이션
 * - 2차원 발사체 운동
 * - 궤적 추적
 * - 최고점/사거리 표시
 */

const params = {
  initialSpeed: 20,        // 초기 속력 (m/s)
  angle: 45,              // 발사 각도 (°)
  gravity: 9.8,           // 중력 가속도 (m/s²)
  airResistance: false,   // 공기 저항 (선택)
};

function calculateProjectile(t) {
  const rad = params.angle * Math.PI / 180;
  const vx = params.initialSpeed * Math.cos(rad);
  const vy = params.initialSpeed * Math.sin(rad) - params.gravity * t;
  const x = vx * t;
  const y = params.initialSpeed * Math.sin(rad) * t - 0.5 * params.gravity * t * t;
  return { x, y, vx, vy };
}

// 특성값 계산
function getCharacteristics() {
  const rad = params.angle * Math.PI / 180;
  const maxHeight = Math.pow(params.initialSpeed * Math.sin(rad), 2) / (2 * params.gravity);
  const range = Math.pow(params.initialSpeed, 2) * Math.sin(2 * rad) / params.gravity;
  const flightTime = 2 * params.initialSpeed * Math.sin(rad) / params.gravity;
  return { maxHeight, range, flightTime };
}
```

### 3. 단진자

#### template-pendulum.jsx
```jsx
/**
 * 단진자 시뮬레이션
 * - 단순 조화 운동
 * - 에너지 보존
 * - 주기 측정
 */

const params = {
  length: 1.0,            // 진자 길이 (m)
  initialAngle: 30,       // 초기 각도 (°)
  gravity: 9.8,           // 중력 가속도 (m/s²)
  damping: 0,             // 감쇠 계수
};

// 소각도 근사 (θ < 15°)
function calculatePendulum_small(t) {
  const omega = Math.sqrt(params.gravity / params.length);
  const theta0 = params.initialAngle * Math.PI / 180;
  const theta = theta0 * Math.cos(omega * t) * Math.exp(-params.damping * t);
  return theta;
}

// 주기 계산
function getPeriod() {
  return 2 * Math.PI * Math.sqrt(params.length / params.gravity);
}
```

### 4. 용수철 진동

#### template-spring.jsx
```jsx
/**
 * 용수철 진동 시뮬레이션
 * - 단순 조화 운동
 * - 에너지 변환 시각화
 */

const params = {
  mass: 1.0,              // 질량 (kg)
  springConstant: 10,     // 용수철 상수 (N/m)
  amplitude: 0.2,         // 진폭 (m)
  damping: 0,             // 감쇠 계수
};

function calculateSpring(t) {
  const omega = Math.sqrt(params.springConstant / params.mass);
  const x = params.amplitude * Math.cos(omega * t) * Math.exp(-params.damping * t);
  const v = -params.amplitude * omega * Math.sin(omega * t) * Math.exp(-params.damping * t);
  
  const KE = 0.5 * params.mass * v * v;
  const PE = 0.5 * params.springConstant * x * x;
  
  return { x, v, KE, PE, totalE: KE + PE };
}
```

### 5. 충돌

#### template-collision.jsx
```jsx
/**
 * 1차원 충돌 시뮬레이션
 * - 탄성/비탄성 충돌
 * - 운동량 보존 확인
 */

const params = {
  mass1: 2,               // 물체1 질량 (kg)
  mass2: 1,               // 물체2 질량 (kg)
  velocity1: 3,           // 물체1 초기 속도 (m/s)
  velocity2: -1,          // 물체2 초기 속도 (m/s)
  restitution: 1.0,       // 반발 계수 (0: 완전 비탄성, 1: 완전 탄성)
};

function calculateCollision() {
  const { mass1: m1, mass2: m2, velocity1: v1, velocity2: v2, restitution: e } = params;
  
  // 충돌 후 속도
  const v1f = ((m1 - e * m2) * v1 + (1 + e) * m2 * v2) / (m1 + m2);
  const v2f = ((m2 - e * m1) * v2 + (1 + e) * m1 * v1) / (m1 + m2);
  
  // 운동량
  const p_before = m1 * v1 + m2 * v2;
  const p_after = m1 * v1f + m2 * v2f;
  
  // 운동 에너지
  const KE_before = 0.5 * m1 * v1 * v1 + 0.5 * m2 * v2 * v2;
  const KE_after = 0.5 * m1 * v1f * v1f + 0.5 * m2 * v2f * v2f;
  
  return { v1f, v2f, p_before, p_after, KE_before, KE_after };
}
```

---

## 파동 (Waves)

### 6. 파동 중첩

#### template-wave-superposition.jsx
```jsx
/**
 * 파동 중첩 시뮬레이션
 * - 두 파동의 합성
 * - 보강/상쇄 간섭
 */

const params = {
  amplitude1: 1,          // 파동1 진폭
  wavelength1: 2,         // 파동1 파장 (m)
  amplitude2: 1,          // 파동2 진폭
  wavelength2: 2,         // 파동2 파장 (m)
  phaseDiff: 0,           // 위상차 (rad)
};

function calculateWave(x, t) {
  const k1 = 2 * Math.PI / params.wavelength1;
  const k2 = 2 * Math.PI / params.wavelength2;
  const omega = 2 * Math.PI; // 단위 주파수
  
  const y1 = params.amplitude1 * Math.sin(k1 * x - omega * t);
  const y2 = params.amplitude2 * Math.sin(k2 * x - omega * t + params.phaseDiff);
  const ySum = y1 + y2;
  
  return { y1, y2, ySum };
}
```

### 7. 정상파

#### template-standing-wave.jsx
```jsx
/**
 * 정상파 시뮬레이션
 * - 현의 진동
 * - n차 조화 진동
 */

const params = {
  length: 1.0,            // 현의 길이 (m)
  harmonic: 1,            // 조화 번호 (n)
  amplitude: 0.1,         // 진폭 (m)
};

function calculateStandingWave(x, t) {
  const n = params.harmonic;
  const L = params.length;
  const wavelength = 2 * L / n;
  const k = 2 * Math.PI / wavelength;
  const omega = 2 * Math.PI; // 단위 주파수
  
  // 정상파: y = 2A sin(kx) cos(ωt)
  const y = 2 * params.amplitude * Math.sin(k * x) * Math.cos(omega * t);
  return y;
}

// 마디/배 위치
function getNodesAndAntinodes() {
  const n = params.harmonic;
  const L = params.length;
  const nodes = [];
  const antinodes = [];
  
  for (let i = 0; i <= n; i++) {
    nodes.push(i * L / n);
  }
  for (let i = 0; i < n; i++) {
    antinodes.push((i + 0.5) * L / n);
  }
  
  return { nodes, antinodes };
}
```

---

## 전자기 (Electromagnetism)

### 8. 전기장 시각화

#### template-electric-field.jsx
```jsx
/**
 * 전기장 시각화
 * - 점전하의 전기장
 * - 전기력선
 * - 등전위선
 */

const charges = [
  { x: -1, y: 0, q: 1 },   // 양전하
  { x: 1, y: 0, q: -1 },   // 음전하
];

const k = 8.99e9; // 쿨롱 상수

function calculateElectricField(px, py) {
  let Ex = 0, Ey = 0;
  
  for (const charge of charges) {
    const dx = px - charge.x;
    const dy = py - charge.y;
    const r = Math.sqrt(dx * dx + dy * dy);
    if (r < 0.01) continue;
    
    const E = k * Math.abs(charge.q) / (r * r);
    const sign = charge.q > 0 ? 1 : -1;
    Ex += sign * E * dx / r;
    Ey += sign * E * dy / r;
  }
  
  return { Ex, Ey, magnitude: Math.sqrt(Ex * Ex + Ey * Ey) };
}

function calculatePotential(px, py) {
  let V = 0;
  for (const charge of charges) {
    const dx = px - charge.x;
    const dy = py - charge.y;
    const r = Math.sqrt(dx * dx + dy * dy);
    if (r < 0.01) continue;
    V += k * charge.q / r;
  }
  return V;
}
```

---

## 현대물리 (Modern Physics)

### 9. 광전효과

#### template-photoelectric.jsx
```jsx
/**
 * 광전효과 시뮬레이션
 * - 문턱 진동수
 * - 광전자 운동 에너지
 */

const params = {
  workFunction: 2.0,      // 일함수 (eV)
  photonEnergy: 3.0,      // 광자 에너지 (eV)
  intensity: 1.0,         // 빛의 세기
};

const h = 4.136e-15;      // 플랑크 상수 (eV·s)
const c = 3e8;            // 광속 (m/s)

function calculatePhotoelectric() {
  const { workFunction: W, photonEnergy: E } = params;
  
  if (E < W) {
    return {
      electronEmitted: false,
      maxKE: 0,
      stoppingVoltage: 0,
    };
  }
  
  const maxKE = E - W;
  const stoppingVoltage = maxKE; // eV 단위이므로 숫자 동일
  
  return {
    electronEmitted: true,
    maxKE,
    stoppingVoltage,
  };
}

function getThresholdFrequency() {
  return params.workFunction / h;
}
```

### 10. 보어 원자 모형

#### template-bohr-model.jsx
```jsx
/**
 * 보어 원자 모형 시뮬레이션
 * - 전자 궤도
 * - 에너지 준위
 * - 전이 스펙트럼
 */

const params = {
  atomicNumber: 1,        // 원자 번호 (수소 = 1)
  currentLevel: 1,        // 현재 에너지 준위
  targetLevel: 2,         // 전이할 준위
};

const bohrRadius = 5.29e-11; // 보어 반지름 (m)
const RydbergEnergy = 13.6;  // 리드베리 에너지 (eV)

function getOrbitRadius(n) {
  return bohrRadius * n * n / params.atomicNumber;
}

function getEnergyLevel(n) {
  return -RydbergEnergy * params.atomicNumber * params.atomicNumber / (n * n);
}

function getTransitionEnergy() {
  const E1 = getEnergyLevel(params.currentLevel);
  const E2 = getEnergyLevel(params.targetLevel);
  return Math.abs(E2 - E1);
}

function getWavelength() {
  const deltaE = getTransitionEnergy();
  const h = 4.136e-15; // eV·s
  const c = 3e8; // m/s
  return h * c / deltaE;
}
```

---

## 2022 개정 교육과정 신규 시뮬레이션

### 11. 돌림힘과 평형 (물리학 신규)

#### template-torque.jsx
```jsx
/**
 * 돌림힘과 평형 시뮬레이션
 * - 지렛대 평형 조건
 * - 무게중심 탐구
 * - 구조물 안정성 분석
 */

const params = {
  pivotPosition: 0.5,     // 받침점 위치 (0~1)
  mass1: 2,               // 왼쪽 물체 질량 (kg)
  distance1: 0.3,         // 왼쪽 거리 (m)
  mass2: 1,               // 오른쪽 물체 질량 (kg)
  distance2: 0.6,         // 오른쪽 거리 (m)
  gravity: 9.8,           // 중력 가속도 (m/s²)
};

function calculateTorque() {
  const torque1 = params.mass1 * params.gravity * params.distance1; // 시계방향
  const torque2 = params.mass2 * params.gravity * params.distance2; // 반시계방향
  const netTorque = torque2 - torque1;
  const isBalanced = Math.abs(netTorque) < 0.01;
  
  return { torque1, torque2, netTorque, isBalanced };
}

// 평형 조건: τ₁ = τ₂, 즉 m₁g·d₁ = m₂g·d₂
```

### 12. 볼록렌즈와 상 (물리학 신규)

#### template-convex-lens.jsx
```jsx
/**
 * 볼록렌즈 상 형성 시뮬레이션
 * - 물체-상 관계
 * - 배율 계산
 * - 실상/허상 구분
 */

const params = {
  focalLength: 0.1,       // 초점거리 (m)
  objectDistance: 0.2,    // 물체거리 (m)
  objectHeight: 0.05,     // 물체 높이 (m)
};

function calculateImage() {
  const { focalLength: f, objectDistance: a, objectHeight: h } = params;
  
  // 렌즈 공식: 1/f = 1/a + 1/b
  const imageDistance = (f * a) / (a - f);
  
  // 배율: m = -b/a = h'/h
  const magnification = -imageDistance / a;
  const imageHeight = magnification * h;
  
  // 상의 특성
  const isReal = imageDistance > 0;
  const isInverted = magnification < 0;
  const isMagnified = Math.abs(magnification) > 1;
  
  return { 
    imageDistance, 
    imageHeight, 
    magnification,
    isReal,      // 실상 여부
    isInverted,  // 도립 여부
    isMagnified  // 확대 여부
  };
}
```

### 13. 탈출 속도 (역학과 에너지 신규)

#### template-escape-velocity.jsx
```jsx
/**
 * 탈출 속도 시뮬레이션
 * - 행성별 탈출 속도 비교
 * - 발사체 운동
 */

const planets = {
  earth: { mass: 5.97e24, radius: 6.37e6, name: '지구' },
  moon: { mass: 7.35e22, radius: 1.74e6, name: '달' },
  mars: { mass: 6.42e23, radius: 3.39e6, name: '화성' },
  jupiter: { mass: 1.90e27, radius: 6.99e7, name: '목성' },
};

const G = 6.674e-11; // 만유인력 상수

function calculateEscapeVelocity(planet) {
  const { mass: M, radius: R } = planets[planet];
  
  // 탈출 속도: v = √(2GM/R)
  const escapeVelocity = Math.sqrt(2 * G * M / R);
  
  return {
    planet: planets[planet].name,
    escapeVelocity,
    escapeVelocityKmS: escapeVelocity / 1000,
  };
}

// 발사체가 탈출하는지 시뮬레이션
function simulateLaunch(planet, initialVelocity) {
  const escapeV = calculateEscapeVelocity(planet).escapeVelocity;
  const willEscape = initialVelocity >= escapeV;
  
  return { willEscape, escapeV, initialVelocity };
}
```

### 14. 중력 시간 지연 (역학과 에너지 신규)

#### template-gravitational-time-dilation.jsx
```jsx
/**
 * 중력 시간 지연 시뮬레이션
 * - GPS 위성 시간 보정
 * - 등가 원리 시각화
 */

const params = {
  earthMass: 5.97e24,      // 지구 질량 (kg)
  earthRadius: 6.37e6,      // 지구 반지름 (m)
  satelliteAltitude: 20200e3, // GPS 위성 고도 (m)
  timePeriod: 86400,        // 하루 (초)
};

const G = 6.674e-11;
const c = 3e8;

function calculateTimeDilation() {
  const { earthMass: M, earthRadius: R, satelliteAltitude: h } = params;
  
  // 지표면에서의 중력 퍼텐셜
  const phiSurface = -G * M / R;
  
  // 위성 궤도에서의 중력 퍼텐셜
  const phiSatellite = -G * M / (R + h);
  
  // 중력 시간 지연 (일반 상대성)
  // Δt/t ≈ (φ₂ - φ₁) / c²
  const gravitationalDilation = (phiSatellite - phiSurface) / (c * c);
  
  // 하루 동안의 시간 차이
  const timeDiffPerDay = gravitationalDilation * params.timePeriod;
  
  return {
    gravitationalDilation,
    timeDiffPerDay,           // 초 단위
    timeDiffMicroseconds: timeDiffPerDay * 1e6,  // 마이크로초
  };
}
```

### 15. 양자 중첩과 측정 (전자기와 양자 신규)

#### template-quantum-superposition.jsx
```jsx
/**
 * 양자 중첩 시뮬레이션
 * - 큐비트 상태 시각화
 * - 측정과 상태 붕괴
 * - 양자컴퓨터 기초
 */

const params = {
  alpha: Math.sqrt(0.5),  // |0⟩ 계수
  beta: Math.sqrt(0.5),   // |1⟩ 계수
  phase: 0,               // 상대 위상 (rad)
};

// 큐비트 상태: |ψ⟩ = α|0⟩ + β·e^(iφ)|1⟩
function getQubitState() {
  const { alpha, beta, phase } = params;
  
  // 확률 계산
  const prob0 = alpha * alpha;
  const prob1 = beta * beta;
  
  // 블로흐 구 좌표
  const theta = 2 * Math.acos(alpha);
  const phi = phase;
  
  return {
    prob0,
    prob1,
    blochSphere: {
      x: Math.sin(theta) * Math.cos(phi),
      y: Math.sin(theta) * Math.sin(phi),
      z: Math.cos(theta),
    }
  };
}

// 측정 시뮬레이션
function measureQubit() {
  const { prob0 } = getQubitState();
  const random = Math.random();
  
  const result = random < prob0 ? 0 : 1;
  
  // 측정 후 상태 붕괴
  return {
    measuredValue: result,
    collapsedState: result === 0 ? '|0⟩' : '|1⟩',
  };
}
```

### 16. 터널 효과 (전자기와 양자 신규)

#### template-quantum-tunneling.jsx
```jsx
/**
 * 터널 효과 시뮬레이션
 * - 장벽 투과 확률
 * - STM 원리
 */

const params = {
  particleMass: 9.11e-31,   // 전자 질량 (kg)
  particleEnergy: 5,        // 입자 에너지 (eV)
  barrierHeight: 10,        // 장벽 높이 (eV)
  barrierWidth: 1e-9,       // 장벽 폭 (m)
};

const hbar = 1.055e-34;     // 환산 플랑크 상수
const eV = 1.602e-19;       // 1 eV in J

function calculateTunnelingProbability() {
  const { particleMass: m, particleEnergy: E, barrierHeight: V0, barrierWidth: L } = params;
  
  // E를 줄(J)로 변환
  const E_J = E * eV;
  const V0_J = V0 * eV;
  
  // κ = √(2m(V₀-E)) / ℏ
  const kappa = Math.sqrt(2 * m * (V0_J - E_J)) / hbar;
  
  // 투과 확률 (근사): T ≈ e^(-2κL)
  const transmissionProb = Math.exp(-2 * kappa * L);
  
  return {
    kappa,
    transmissionProb,
    transmissionPercent: transmissionProb * 100,
    reflectionProb: 1 - transmissionProb,
  };
}
```

### 17. 핵융합과 별 (전자기와 양자 신규)

#### template-stellar-fusion.jsx
```jsx
/**
 * 핵융합 시뮬레이션
 * - 양성자-양성자 체인
 * - 질량-에너지 등가
 * - 별의 스펙트럼
 */

const protonMass = 1.6726e-27;  // kg
const neutronMass = 1.6749e-27; // kg
const electronMass = 9.109e-31; // kg
const c = 3e8;                  // 광속 m/s

// pp chain: 4H → He + 2e⁺ + 2νₑ + γ
function calculateFusionEnergy() {
  // 4개 수소 원자핵 질량
  const mass4H = 4 * protonMass;
  
  // 헬륨-4 원자핵 질량 (실제값)
  const massHe4 = 6.6447e-27;
  
  // 질량 결손
  const deltaMass = mass4H - massHe4;
  
  // 방출 에너지: E = Δmc²
  const energyReleased = deltaMass * c * c;
  const energyMeV = energyReleased / (1.602e-13);
  
  return {
    deltaMass,
    energyReleased,      // Joules
    energyMeV,           // MeV (약 26.7 MeV)
  };
}

// 별의 광도 계산 (태양 기준)
function calculateLuminosity(mass_solar) {
  // 질량-광도 관계: L ∝ M^3.5 (주계열성)
  const luminosity_solar = Math.pow(mass_solar, 3.5);
  const luminosity_watts = luminosity_solar * 3.828e26;
  
  return { luminosity_solar, luminosity_watts };
}
```

---

### Controls.jsx
```jsx
/**
 * 공통 조작 패널 컴포넌트
 */

function Slider({ label, value, min, max, step, onChange, unit }) {
  return (
    <div className="slider-control">
      <label>{label}: {value.toFixed(2)} {unit}</label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
      />
    </div>
  );
}

function PlaybackControls({ isPlaying, onPlay, onPause, onReset }) {
  return (
    <div className="playback-controls">
      <button onClick={isPlaying ? onPause : onPlay}>
        {isPlaying ? '⏸ 정지' : '▶ 시작'}
      </button>
      <button onClick={onReset}>↺ 초기화</button>
    </div>
  );
}
```

### Graph.jsx
```jsx
/**
 * 실시간 그래프 컴포넌트
 */

function RealtimeGraph({ data, xLabel, yLabel, title }) {
  // Recharts 또는 Chart.js 사용
  return (
    <div className="graph-container">
      <h3>{title}</h3>
      <LineChart data={data}>
        <XAxis dataKey="x" label={xLabel} />
        <YAxis label={yLabel} />
        <Line type="monotone" dataKey="y" stroke="#8884d8" />
      </LineChart>
    </div>
  );
}
```
