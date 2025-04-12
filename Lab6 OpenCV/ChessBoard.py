# 导入相关库
import cv2
import numpy as np

# 棋盘定位

原图 = cv2.imread('board.png')
灰度图 = cv2.cvtColor(原图, cv2.COLOR_BGR2GRAY)
高斯模糊图 = cv2.GaussianBlur(灰度图, (5, 5), 0)
边缘图 = cv2.Canny(高斯模糊图, 50, 150)

轮廓, _ = cv2.findContours(边缘图, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
最大轮廓 = max(轮廓, key=cv2.contourArea)

内接矩形 = cv2.minAreaRect(最大轮廓)
四角坐标 = cv2.boxPoints(内接矩形)
四角坐标 = np.intp(四角坐标)
print(四角坐标)

棋盘定位图 = 原图.copy()
cv2.drawContours(棋盘定位图, [四角坐标], 0, (0, 0, 255), 3)
for point in 四角坐标:
    cv2.circle(棋盘定位图, tuple(point), 5, (0, 255, 0), -1)


# 棋子颜色判断函数
def black_or_white(img, x, y, r):
    mask = np.zeros(img.shape[:2], dtype=np.uint8)  # 创建掩膜, 黑色背景
    cv2.circle(mask, (x, y), r, 255, -1)  # 画圆形区域
    mean_color = cv2.mean(img, mask=mask)  # 计算平均颜色
    if mean_color[0] > 192:
        return 1  # 白色棋子
    if mean_color[0] < 64:
        return 2  # 黑色棋子
    else:
        return 0  # 无棋子


# 棋子定位, 同时判断颜色

圆形检测 = cv2.HoughCircles(高斯模糊图, cv2.HOUGH_GRADIENT, 1, 15, param1=100, param2=12, minRadius=11, maxRadius=16)
棋盘矩阵 = np.zeros((19, 19), dtype=int)
棋子高亮图 = 棋盘定位图.copy()

for circle in 圆形检测[0]:
    x, y, r = circle
    x = int(x)
    y = int(y)
    r = int(r)
    row = round((y-四角坐标[0][1])/(四角坐标[2][1]-四角坐标[0][1]) * 18)
    col = round((x-四角坐标[0][0])/(四角坐标[2][0]-四角坐标[0][0]) * 18)
    color = black_or_white(原图, x, y, r)  # 判断棋子颜色

    棋盘矩阵[row][col] = color  # 判断棋子颜色并存入棋盘矩阵
    if color == 1:
        cv2.circle(棋子高亮图, (x, y), r, (0, 0, 255), 2)
        cv2.putText(棋子高亮图, f'({row}, {col})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    elif color == 2:
        cv2.circle(棋子高亮图, (x, y), r, (0, 255, 0), 2)
        cv2.putText(棋子高亮图, f'({row}, {col})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
cv2.imshow('circles', 棋子高亮图)

print(棋盘矩阵)

# 五子棋判定
def check_win(board, x, y):
    color = board[x][y]
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、对角线、反对角线
    for dx, dy in directions:
        count = 1
        for step in range(1, 5):  # 向一个方向检查
            nx, ny = x + dx * step, y + dy * step
            if 0 <= nx < 19 and 0 <= ny < 19 and board[nx][ny] == color:
                count += 1
            else:
                break
        for step in range(1, 5):  # 向另一个方向检查
            nx, ny = x - dx * step, y - dy * step
            if 0 <= nx < 19 and 0 <= ny < 19 and board[nx][ny] == color:
                count += 1
            else:
                break
        if count >= 5:  # 如果连成五子，返回True
            return True
    return False


# 棋盘矩阵中查找五子连珠
winner = 0
for i in range(19):
    for j in range(19):
        if 棋盘矩阵[i][j] != 0 and check_win(棋盘矩阵, i, j):
            winner = 棋盘矩阵[i][j]
            break
        
if winner == 1:
    print('白棋胜利')
elif winner == 2:
    print('黑棋胜利')
else:
    print('平局')


cv2.waitKey(0)
cv2.destroyAllWindows()

