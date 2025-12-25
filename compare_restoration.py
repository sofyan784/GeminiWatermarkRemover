import os

def get_size(path):
    if os.path.exists(path):
        return os.path.getsize(path)
    return -1

s_out_left = get_size("output_left.png")
s_right = get_size("sample_right.png")

print(f"Output Left: {s_out_left}")
print(f"Sample Right: {s_right}")

# Simple size comparison isn't enough, but if they are close, it's a good sign.
# Ideally we'd do a pixel diff, but without numpy/cv2 installed in python env (maybe), we can't easily.
# But I can check if they are identical bytes.
if s_out_left == s_right:
    print("Sizes identical.")
else:
    print("Sizes differ.")
