import cv2
import numpy as np
from collections import deque


class AIRefereeDemo:
    def __init__(self):
        self.positions = deque(maxlen=8)
        self.last_decision = "READY"
        self.goal_count = 0

        # 화면 기준 가상 판정선 비율
        self.goal_line_ratio = 0.82
        self.out_margin_ratio = 0.08

    def detect_ball(self, frame):
        """
        초록색/형광색 물체를 공으로 인식하는 단순 데모입니다.
        실제 프로젝트에서는 YOLO 같은 객체 탐지 모델로 교체할 수 있습니다.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 초록색 범위. 형광 초록 공/물체를 쓰면 잘 잡힙니다.
        lower_green = np.array([35, 60, 60])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None, mask

        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        # 너무 작은 잡음 제거
        if area < 400:
            return None, mask

        (x, y), radius = cv2.minEnclosingCircle(largest_contour)

        if radius < 8:
            return None, mask

        return (int(x), int(y), int(radius)), mask

    def estimate_speed(self):
        if len(self.positions) < 2:
            return 0

        x1, y1 = self.positions[-2]
        x2, y2 = self.positions[-1]

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        return distance

    def make_decision(self, ball, width, height):
        """
        공 위치를 바탕으로 간단한 심판 판정을 수행합니다.
        """
        if ball is None:
            self.last_decision = "NO BALL DETECTED"
            return self.last_decision

        x, y, radius = ball
        self.positions.append((x, y))

        goal_line_x = int(width * self.goal_line_ratio)
        out_top = int(height * self.out_margin_ratio)
        out_bottom = int(height * (1 - self.out_margin_ratio))

        speed = self.estimate_speed()

        if x >= goal_line_x:
            self.last_decision = "GOAL"
            self.goal_count += 1
        elif y <= out_top or y >= out_bottom:
            self.last_decision = "OUT"
        elif speed > 40:
            self.last_decision = "FAST PLAY"
        else:
            self.last_decision = "PLAY ON"

        return self.last_decision

    def draw_overlay(self, frame, ball, decision):
        height, width = frame.shape[:2]

        goal_line_x = int(width * self.goal_line_ratio)
        out_top = int(height * self.out_margin_ratio)
        out_bottom = int(height * (1 - self.out_margin_ratio))

        # 가상 골라인
        cv2.line(frame, (goal_line_x, 0), (goal_line_x, height), (0, 255, 255), 3)
        cv2.putText(frame, "GOAL LINE", (goal_line_x - 120, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # 아웃 라인
        cv2.line(frame, (0, out_top), (width, out_top), (255, 0, 0), 2)
        cv2.line(frame, (0, out_bottom), (width, out_bottom), (255, 0, 0), 2)
        cv2.putText(frame, "OUT ZONE", (20, out_top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # 공 표시
        if ball is not None:
            x, y, radius = ball
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 3)
            cv2.circle(frame, (x, y), 4, (0, 0, 255), -1)
            cv2.putText(frame, "BALL", (x - 30, y - radius - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # 판정 표시
        cv2.rectangle(frame, (0, 0), (width, 75), (0, 0, 0), -1)
        cv2.putText(frame, f"AI REFEREE: {decision}", (20, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 3)

        cv2.putText(frame, f"Goals: {self.goal_count}", (20, height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        return frame


def main():
    referee = AIRefereeDemo()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("웹캠을 열 수 없습니다. 카메라 권한이나 연결 상태를 확인하세요.")
        return

    print("AI Autonomous Sports Referee Demo 시작")
    print("초록색 공/물체를 웹캠 앞에서 움직여보세요.")
    print("종료: q 키")

    while True:
        ret, frame = camera.read()

        if not ret:
            print("웹캠 프레임을 읽을 수 없습니다.")
            break

        # 좌우 반전: 거울처럼 보기 편하게
        frame = cv2.flip(frame, 1)

        ball, mask = referee.detect_ball(frame)
        decision = referee.make_decision(ball, frame.shape[1], frame.shape[0])
        output = referee.draw_overlay(frame, ball, decision)

        cv2.imshow("AI Autonomous Sports Referee Demo", output)
        cv2.imshow("Ball Detection Mask", mask)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
