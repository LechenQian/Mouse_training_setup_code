import cv2
# os.system("v4l2-ctl -i 5 -s 5")


cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

#
# # vc.set(cv2.CAP_FFMPEG,True)
# # vc.set(cv2.CAP_PROP_FORMAT,1)
# vc.set(cv2.CAP_PROP_FPS,8)
# if vc.isOpened(): # try to get the first frame
#     rval, frame = vc.read()
# else:
#     rval = False
#
# while rval:
#
#     rval, frame = vc.read()
#
#     cv2.imshow("preview", frame)
#
#     key = cv2.waitKey(20)
#     if key == 27: # exit on ESC
#         break
# vc.release()
cv2.destroyWindow("preview")