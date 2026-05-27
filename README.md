# AI Autonomous Sports Referee ⚽🤖

웹캠과 AI 비전 기술을 활용해 스포츠 경기의 일부 상황을 자동으로 판정하는 미래형 무인 심판 시스템 데모입니다.

## 프로젝트 소개

이 프로젝트는 미래직업 아이디어 대회를 위해 기획한 AI 완전자동화 심판 시스템입니다.

노트북 웹캠으로 경기 화면을 입력받고, OpenCV를 이용해 공의 위치를 추적한 뒤 가상 골라인과 아웃라인을 기준으로 판정을 내립니다.

초기 버전은 색상 기반 공 추적 방식으로 구현되었으며, 향후 YOLO 객체 탐지, 선수 자세 인식, 충돌 감지, 규칙 엔진으로 확장할 수 있습니다.

## 주요 기능

- 노트북 웹캠 입력
- 초록색 공 또는 물체 추적
- 가상 골라인 판정
- 아웃라인 판정
- 빠른 움직임 감지
- 화면 위 AI 심판 판정 표시

## 사용 기술

- Python
- OpenCV
- NumPy
- Webcam
- Computer Vision

## 시스템 구조

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
