import cv2


def nothing(*args):
    pass


def paint_contours(frame, lower_color, upper_color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.bitwise_not(mask)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        biggest_contour = max(contours, key=cv2.contourArea)
        print(f'area = {cv2.contourArea(biggest_contour)}')
        x, y, w, h = cv2.boundingRect(biggest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        print(f'len = {w}, height = {h}')
    else:
        print(f'{e}: объектов не найдено')
    return frame, mask


def webcam():
    cap = cv2.VideoCapture(0)

    cv2.namedWindow('window')

    cv2.createTrackbar('H Lower', 'window', 0, 179, nothing)
    cv2.createTrackbar('H Upper', 'window', 179, 179, nothing)
    cv2.createTrackbar('S Lower', 'window', 0, 255, nothing)
    cv2.createTrackbar('S Upper', 'window', 255, 255, nothing)
    cv2.createTrackbar('V Lower', 'window', 0, 255, nothing)
    cv2.createTrackbar('V Upper', 'window', 255, 255, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h_lower = cv2.getTrackbarPos('H Lower', 'window')
        h_upper = cv2.getTrackbarPos('H Upper', 'window')
        s_lower = cv2.getTrackbarPos('S Lower', 'window')
        s_upper = cv2.getTrackbarPos('S Upper', 'window')
        v_lower = cv2.getTrackbarPos('V Lower', 'window')
        v_upper = cv2.getTrackbarPos('V Upper', 'window')

        lower_color = (h_lower, s_lower, v_lower)
        upper_color = (h_upper, s_upper, v_upper)

        frame, mask = paint_contours(frame, lower_color, upper_color)

        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    webcam()
