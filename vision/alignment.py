import cv2
import numpy as np

# Jordan laptop camera contstants
half_y_fov = np.tan((0.5 * 12.25) / 15)
half_x_fov = np.tan((0.5 * 22) / 15)


def annotate_alignment(img_use):
    half_y = (img_use.shape[0] / 2)
    half_x = (img_use.shape[1] / 2)

    img_hsv = cv2.cvtColor(img_use, cv2.COLOR_BGR2HSV)
    lower_hoop = np.array([4, 100, 75]) #175
    upper_hoop = np.array([15, 255, 255])
    hoop_mask = cv2.inRange(img_hsv, lower_hoop, upper_hoop)

    opening_kernel = np.ones((5, 5), dtype=np.uint8)
    hoop_mask = cv2.morphologyEx(hoop_mask.astype(np.uint8), cv2.MORPH_OPEN, opening_kernel)

    closing_kernel = np.ones((60, 60), dtype=np.uint8)
    hoop_mask = cv2.morphologyEx(hoop_mask, cv2.MORPH_CLOSE, closing_kernel)

    hoop_contours, hoop_heirarchies = cv2.findContours(hoop_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cv2.circle(img_use, (int(half_x), int(half_y)), radius=20, color=(0, 0, 0), thickness=-1)

    if len(hoop_contours) > 0:
        largest_contour = np.argmax([
            cv2.contourArea(hoop_contour) for hoop_contour in hoop_contours
        ])
        largest_contour = hoop_contours[largest_contour]

        hoop_bounding_boxes = cv2.boundingRect(largest_contour)
 
        top_left_x, top_left_y, width, height = hoop_bounding_boxes
        cv2.rectangle(
            img_use,
            (top_left_x, top_left_y), (top_left_x + width, top_left_y + height),
            (0, 255, 0),
            5
        )
        try:
            hoop_ellipses = cv2.fitEllipse(largest_contour)
            cv2.ellipse(img_use, hoop_ellipses, (255, 0, 0), 4)
        except:
            pass

        # Get centroid
        contour_moments = cv2.moments(largest_contour)
        contour_center_x = int(contour_moments['m10'] / contour_moments['m00'])
        contour_center_y = int(contour_moments['m01'] / contour_moments['m00'])

        cv2.circle(
            img_use, (contour_center_x, contour_center_y),
            radius=20, color=(0, 255, 0), thickness=-1
        )

        aim_x = (contour_center_x - half_x) / half_x
        aim_y = (contour_center_y - half_y) / half_y

        yaw = aim_x * half_x_fov # horizontal alignment
        pitch = aim_y * half_y_fov # vertical alignment
        distance = 26.5 / np.tan(np.radians(0) + pitch) # angular distance; convert to
        # horizontal

        cv2.putText(
            img_use, f"Pitch (vertical): {'{:.2f}'.format(np.degrees(-pitch))} d",
            (10, 75), cv2.FONT_HERSHEY_SIMPLEX,
            2, (0, 255, 0), thickness=5
        )
        cv2.putText(
            img_use, f"Yaw (horizontal): {'{:.2f}'.format(np.degrees(yaw))} d",
            (10, 175), cv2.FONT_HERSHEY_SIMPLEX,
            2, (0, 255, 0), thickness=5
        )

        cv2.putText(
            img_use, f"Distance: {'{:.2f}'.format(distance)}in",
            (10, 275), cv2.FONT_HERSHEY_SIMPLEX,
            2, (0, 255, 0), thickness=5
        )

    cv2.putText(
        img_use, f"FOV Vertical: {'{:.0f}'.format(np.degrees(half_y_fov * 2))} d",
        (10, img_use.shape[0] - 140), cv2.FONT_HERSHEY_SIMPLEX,
        2, (0, 255, 0), thickness=5
    )
    cv2.putText(
        img_use, f"FOV Horizontal: {'{:.0f}'.format(np.degrees(half_x_fov * 2))} d",
        (10, img_use.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX,
        2, (0, 255, 0), thickness=5
    )

    return img_use

cap = cv2.VideoCapture('WIN_20240113_14_59_09_Pro.mp4')
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(
    'test_alignment_distance_slow.avi', fourcc, 10, #29.59686363519125 #10
    (int(cap.get(3)),int(cap.get(4)))
)

i = 0
while cap.isOpened():
    ret, img = cap.read()
    
    if not ret:
        break

    annotated_img = annotate_alignment(img)
    out.write(annotated_img)

    c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):
        break

    i += 1
    if i > 270:
        break

cap.release()
out.release()
cv2.destroyAllWindows()