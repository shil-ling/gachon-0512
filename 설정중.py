import mediapipe
import os

print("--- 범인 추적 결과 ---")
print(f"파이썬이 인식한 mediapipe 위치: {mediapipe.__file__}")
print(f"현재 실행 중인 폴더 위치: {os.getcwd()}")
print("----------------------")