

import cv2
import time
import keyboard
import platform
import numpy as np
import mediapipe as mp
from pynput.mouse import Button, Controller

from nonmouse.args import *
from nonmouse.utils import *

mouse = Controller()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

pf = platform.system()


def main():
    cap_device, mode, kando, screenRes = tk_arg()
    dis = 0.7                           # くっつける距離の定義
    preX, preY = 0, 0
    nowCli, preCli = 0, 0               # 現在、前回の左クリック状態
    norCli, prrCli = 0, 0               # 現在、前回の右クリック状態
    douCli = 0                          # ダブルクリック状態
    i, k, h = 0, 0, 0
    LiTx, LiTy, list0x, list0y, list1x, list1y, list4x, list4y, list6x, list6y, list8x, list8y, list12x, list12y = [
    ], [], [], [], [], [], [], [], [], [], [], [], [], []   # 移動平均用リスト
    moving_average = [[0] * 3 for _ in range(3)]
    nowUgo = 1
    cap_width = 1280
    cap_height = 720
    start, c_start = float('inf'), float('inf')
    c_text = 0
    # Beautiful window setup
    window_name = 'NonMouse'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1400, 1000)
    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FPS, 60)
    cfps = int(cap.get(cv2.CAP_PROP_FPS))
    if cfps < 30:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)
        cfps = int(cap.get(cv2.CAP_PROP_FPS))
    # スムージング量（小さい:カーソルが小刻みに動く 大きい:遅延が大）
    ran = max(int(cfps/10), 1)
    hands = mp_hands.Hands(
        min_detection_confidence=0.8,   # 検出信頼度
        min_tracking_confidence=0.8,    # 追跡信頼度
        max_num_hands=1                 # 最大検出数
    )
    # メインループ ###############################################################################
    while cap.isOpened():
        p_s = time.perf_counter()
        success, image = cap.read()
        if not success:
            continue
        if mode == 1:                   # Mouse
            image = cv2.flip(image, 0)  # 上下反転
        elif mode == 2:                 # Touch
            image = cv2.flip(image, 1)  # 左右反転

        # 画像を水平方向に反転し、BGR画像をRGBに変換
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False   # 参照渡しのためにイメージを書き込み不可としてマーク
        results = hands.process(image)  # mediapipeの処理
        image.flags.writeable = True    # 画像に手のアノテーションを描画
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape

        if results.multi_hand_landmarks:
            # 手の骨格描画
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if pf == 'Linux':           # Linuxだったら、常に動かす
                can = 1
                c_text = 0
            else:                       # Windows/macOSでも常に動かす
                can = 1
                c_text = 0
            # グローバルホットキーが押されているとき ##################################################
            if can == 1:
                # print(hand_landmarks.landmark[0])
                # preX, preYに現在のマウス位置を代入 1回だけ実行
                if i == 0:
                    preX = hand_landmarks.landmark[8].x
                    preY = hand_landmarks.landmark[8].y
                    i += 1

                # 以下で使うランドマーク座標の移動平均計算
                landmark0 = [calculate_moving_average(hand_landmarks.landmark[0].x, ran, list0x), calculate_moving_average(
                    hand_landmarks.landmark[0].y, ran, list0y)]
                landmark1 = [calculate_moving_average(hand_landmarks.landmark[1].x, ran, list1x), calculate_moving_average(
                    hand_landmarks.landmark[1].y, ran, list1y)]
                landmark4 = [calculate_moving_average(hand_landmarks.landmark[4].x, ran, list4x), calculate_moving_average(
                    hand_landmarks.landmark[4].y, ran, list4y)]
                landmark6 = [calculate_moving_average(hand_landmarks.landmark[6].x, ran, list6x), calculate_moving_average(
                    hand_landmarks.landmark[6].y, ran, list6y)]
                landmark8 = [calculate_moving_average(hand_landmarks.landmark[8].x, ran, list8x), calculate_moving_average(
                    hand_landmarks.landmark[8].y, ran, list8y)]
                landmark12 = [calculate_moving_average(hand_landmarks.landmark[12].x, ran, list12x), calculate_moving_average(
                    hand_landmarks.landmark[12].y, ran, list12y)]

                # 指相対座標の基準距離、以後mediapipeから得られた距離をこの値で割る
                absKij = calculate_distance(landmark0, landmark1)
                # 人差し指の先端と中指の先端間のユークリッド距離
                absUgo = calculate_distance(landmark8, landmark12) / absKij
                # 人差し指の第２関節と親指の先端間のユークリッド距離
                absCli = calculate_distance(landmark4, landmark6) / absKij

                posx, posy = mouse.position

                # 人差し指の先端をカーソルに対応
                # カメラ座標をマウス移動量に変換
                nowX = calculate_moving_average(
                    hand_landmarks.landmark[8].x, ran, LiTx)
                nowY = calculate_moving_average(
                    hand_landmarks.landmark[8].y, ran, LiTy)

                dx = kando * (nowX - preX) * image_width
                dy = kando * (nowY - preY) * image_height

                if pf == 'Windows' or pf == 'Linux':     # Windows,linuxの場合、マウス移動量に0.5を足して補正
                    dx = dx+0.5
                    dy = dy+0.5
                preX = nowX
                preY = nowY
                # print(dx, dy)
                if posx+dx < 0:  # カーソルがディスプレイから出て戻ってこなくなる問題の防止
                    dx = -posx
                elif posx+dx > screenRes[0]:
                    dx = screenRes[0]-posx
                if posy+dy < 0:
                    dy = -posy
                elif posy+dy > screenRes[1]:
                    dy = screenRes[1]-posy

                # フラグ #########################################################################
                # click状態
                if absCli < dis:
                    nowCli = 1          # nowCli:左クリック状態(1:click  0:non click)
                    draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                hand_landmarks.landmark[8].y * image_height, 20, (0, 250, 250))
                elif absCli >= dis:
                    nowCli = 0
                if np.abs(dx) > 7 and np.abs(dy) > 7:
                    k = 0                           # 「動いている」ときk=0
                # 右クリック状態 １秒以上クリック状態&&カーソルを動かさない
                # 「動いていない」ときでクリックされたとき
                if nowCli == 1 and np.abs(dx) < 7 and np.abs(dy) < 7:
                    if k == 0:          # k:クリック状態&&カーソルを動かしてない。113, 140行目でk=0にする
                        start = time.perf_counter()
                        k += 1
                    end = time.perf_counter()
                    if end-start > 1.5:
                        norCli = 1
                        draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                    hand_landmarks.landmark[8].y * image_height, 20, (0, 0, 250))
                else:
                    norCli = 0

                # Fixed finger counting function
                def count_fingers_up(landmarks):
                    fingers = []
                    # Thumb - check if tip is to the right of joint (for right hand)
                    if landmarks[4].x > landmarks[3].x:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    # Other fingers - check if tip is above PIP joint
                    for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:
                        if landmarks[tip].y < landmarks[pip].y:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    return fingers
                
                # Gesture detection with more flexible conditions
                fingers_up = count_fingers_up(hand_landmarks.landmark)
                finger_count = sum(fingers_up)
                
                # V gesture: 2 fingers up (index and middle)
                if finger_count == 2 and fingers_up[1] == 1 and fingers_up[2] == 1:
                    current_time = time.perf_counter()
                    if current_time - c_start > 2.0:
                        from pynput.keyboard import Key, Controller as KeyboardController
                        kbd = KeyboardController()
                        kbd.press(Key.ctrl)
                        kbd.press('v')
                        kbd.release('v')
                        kbd.release(Key.ctrl)
                        c_start = current_time
                        cv2.putText(image, "PASTE!", (image_width//2-50, image_height//2), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                
                # Fist gesture: no fingers up
                elif finger_count == 0:
                    current_time = time.perf_counter()
                    if current_time - c_start > 2.0:
                        from pynput.keyboard import Key, Controller as KeyboardController
                        kbd = KeyboardController()
                        kbd.press(Key.ctrl)
                        kbd.press('c')
                        kbd.release('c')
                        kbd.release(Key.ctrl)
                        c_start = current_time
                        cv2.putText(image, "COPY!", (image_width//2-50, image_height//2), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
                # cursor movement - always move when hand is detected
                if nowUgo == 1 and (abs(dx) > 1 or abs(dy) > 1):
                    mouse.move(dx, dy)
                    draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                hand_landmarks.landmark[8].y * image_height, 8, (250, 0, 0))
                # left click
                if nowCli == 1 and nowCli != preCli:
                    if h == 1:                                  # 右クリック終わった直後状態：左クリックしない
                        h = 0
                    elif h == 0:                                # 普段の状態
                        mouse.press(Button.left)
                    # print('Click')
                # left click release
                if nowCli == 0 and nowCli != preCli:
                    mouse.release(Button.left)
                    k = 0
                    # print('Release')
                    if douCli == 0:                             # 1回目のクリックが終わったら、時間測る
                        c_start = time.perf_counter()
                        douCli += 1
                    c_end = time.perf_counter()
                    if 10*(c_end-c_start) > 5 and douCli == 1:  # 0.5秒以内にもう一回クリックしたらダブルクリック
                        mouse.click(Button.left, 2)             # double click
                        douCli = 0
                # right click
                if norCli == 1 and norCli != prrCli:
                    # mouse.release(Button.left)                # 何故か必要
                    mouse.press(Button.right)
                    mouse.release(Button.right)
                    h = 1                                       # 右クリック終わった直後状態h=1
                    # print("right click")
                # scroll - when index finger is lowered
                if hand_landmarks.landmark[8].y > hand_landmarks.landmark[5].y + 0.05:
                    mouse.scroll(0, -dy/30)
                    draw_circle(image, hand_landmarks.landmark[8].x * image_width,
                                hand_landmarks.landmark[8].y * image_height, 20, (0, 0, 0))
                    nowUgo = 0
                else:
                    nowUgo = 1

                preCli = nowCli
                prrCli = norCli

        # Minimal Modern GUI
        h, w = image_height, image_width
        
        # Dark overlay for clean look
        overlay = image.copy()
        cv2.rectangle(overlay, (0, 0), (w, 80), (20, 20, 20), -1)
        cv2.rectangle(overlay, (0, h-120), (w, h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.8, image, 0.2, 0, image)
        
        # Top bar - brand and status
        cv2.putText(image, "NonMouse", (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        
        # Status dot
        status_color = (0, 255, 100) if results.multi_hand_landmarks else (255, 80, 80)
        cv2.circle(image, (w-60, 40), 15, status_color, -1)
        
        # FPS counter
        p_e = time.perf_counter()
        fps = int(1/(p_e - p_s)) if (p_e - p_s) > 0 else 0
        cv2.putText(image, f"{fps}", (w-120, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
        
        # Bottom status bar
        if results.multi_hand_landmarks:
            action = "Ready"
            if nowCli == 1: action = "Click"
            elif norCli == 1: action = "Right"
            elif not nowUgo: action = "Scroll"
        else:
            action = "Show Hand"
        
        cv2.putText(image, action, (w//2-50, h-40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        
        # Gesture guide - corner overlay
        if results.multi_hand_landmarks:
            def count_fingers_up(landmarks):
                fingers = []
                if landmarks[4].x > landmarks[3].x: fingers.append(1)
                else: fingers.append(0)
                for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:
                    if landmarks[tip].y < landmarks[pip].y: fingers.append(1)
                    else: fingers.append(0)
                return fingers
            
            fingers_up = count_fingers_up(hand_landmarks.landmark)
            finger_count = sum(fingers_up)
            
            cv2.putText(image, f"Fingers: {finger_count}", (30, h-80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Clean hand visualization - minimal dots only
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for idx in [4, 8, 12, 16, 20]:  # Fingertips only
                    x = int(hand_landmarks.landmark[idx].x * w)
                    y = int(hand_landmarks.landmark[idx].y * h)
                    cv2.circle(image, (x, y), 6, (255, 255, 255), -1)
                    cv2.circle(image, (x, y), 8, (100, 200, 255), 2)
        # High-resolution display
        cv2.imshow(window_name, cv2.resize(image, dsize=None, fx=0.9, fy=0.9))
        if (cv2.waitKey(1) & 0xFF == 27) or (cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) == 0):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
