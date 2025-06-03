#làm xong tất cả các phần rồi import vào file này rồi chạy ứng dụng
import GiaoDien
if __name__ == "__main__":
    GiaoDien.showProgram();

#1 số test case để test chương trình
# 1.10a (có nghiệm)
# min -x1 + x2
# -x1 -2x2 <= 6
# x1 - 2x2 <= 4
# -x1 + x2 <= 1
# x1 <=0 
# x2 <= 0

# 1.10b (vsn - hình chú thích là đoạn màu đen)
# max x1 - x2
# 3x1 + x2 >= 3
# x1 + 2x2 >= 4
# x1 - x2 <= 1
# x1 <= 5
# x2 <= 5

# 1.10c (có nghiệm)
# max 5x1 +6x2
# x1 - 2x2 >= 2
# -2x1 + 3x2 >= 2

# 1.10d (có nghiệm)
# min -2x1 -x2
# x1 +2x2 <= 6
# x1 - x2 >= 3
# x1 >= 0
# x2 >= 0

# 1.12 (vn)
# max 3x1 +2x2
# 2x1 + x2 <= 2
# 3x1 + 4x2 >= 12
# x1 >= 0
# x2 >= 0

# test 2 pha:
# max 2x1 - 6x2 
# -x1 - x2 - x3 <= -2
# 2x1 - x2 + x3 <= 1
# x1 >= 0
# x2 >= 0
# x3 >= 0


# test case đơn hình, bland, hình học:
# max  4x1 + 5x2 
# 2x1 + 2x2 <= 9
# x1 <= 4
# x2 <= 3
# x1 >= 0
# x2 >= 0

# min -2x1 - x2
# 3x1 + x2 <= 3
# x1 >= 0
# x2 >= 0

# max 3x1 + 5x2
# x1 + 2x2 <= 5
# x1 <= 3
# x2 <= 2
# x1 >= 0
# x2 >= 0

# min -10x1 + 57x2 + 9x3 + 24x4 - 100x5
# 0.5x1 - 5.5x2 - 2.5x3 + 9x4 + x5 <= 1
# 0.5x1 - 1.5x2 - 0.5x3 + x4 + x5 <= 1
# x1 + x5 <= 1
# x5 <= 1
# x1 >= 0
# x2 >= 0
# x3 >= 0
# x4 >= 0
# x5 >= 0
