import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import filedialog

# 1. 파일 선택 (초보자에게 가장 직관적인 방식)
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

if not file_path:
    print("사진을 선택하지 않았습니다.")
    exit()

# 2. 가장 표준적인 초기화 방식
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

# 3. 이미지 처리
img = cv2.imread(file_path)
if img is None:
    print("이미지를 읽을 수 없습니다.")
    exit()

results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# 4. 손가락 개수 세기 논리
if results.multi_hand_landmarks:
    for hand_lms in results.multi_hand_landmarks:
        # 손가락 끝 번호 리스트
        tip_ids = [4, 8, 12, 16, 20]
        fingers = []

        # 엄지 (좌우 비교)
        if hand_lms.landmark[tip_ids[0]].x > hand_lms.landmark[tip_ids[0]-1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # 나머지 네 손가락 (상하 비교)
        for i in range(1, 5):
            if hand_lms.landmark[tip_ids[i]].y < hand_lms.landmark[tip_ids[i]-2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        total = fingers.count(1)
        
        # 화면 표시
        mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
        cv2.putText(img, f'Count: {total}', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)

    cv2.imshow("Hand Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("손을 찾을 수 없습니다. 다른 사진으로 시도해 보세요.")