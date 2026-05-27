# System Architecture

## 전체 구조

이 프로젝트는 노트북 웹캠 입력을 받아 공의 위치를 추적하고, 가상 경기 규칙을 적용해 심판 판정을 내리는 AI 심판 데모입니다.

```txt
Webcam Input
      ↓
Ball Detection
      ↓
Position Tracking
      ↓
Rule Engine
      ↓
AI Referee Decision
      ↓
Screen Display
```

## 주요 구성 요소

### Webcam Input

노트북 웹캠으로 경기 상황을 입력받습니다.

### Ball Detection

OpenCV를 이용해 초록색 공 또는 형광색 물체를 탐지합니다.

### Position Tracking

공의 위치 변화를 추적해 골라인, 아웃라인, 빠른 움직임 여부를 판단합니다.

### Rule Engine

가상 골라인과 아웃라인을 기준으로 GOAL, OUT, PLAY ON, FAST PLAY 판정을 내립니다.

### Screen Display

웹캠 화면 위에 AI 심판 판정 결과를 실시간으로 표시합니다.

## 향후 확장

- YOLO 기반 공/선수 탐지
- 선수 충돌 및 반칙 감지
- 여러 대의 카메라 활용
- 실제 경기 규칙 엔진 추가
- 판정 결과 전광판 출력
