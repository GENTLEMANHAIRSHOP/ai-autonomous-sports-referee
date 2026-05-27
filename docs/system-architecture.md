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
