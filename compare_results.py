import os

def get_size(path):
    if os.path.exists(path):
        return os.path.getsize(path)
    return -1

files = [
    ("sample_left.png", "output_left.png"),
    ("sample_right.png", "output_right.png")
]

for inp, out in files:
    s_in = get_size(inp)
    s_out = get_size(out)
    print(f"{inp} ({s_in}) vs {out} ({s_out})")
    if s_in != s_out:
        print(f"  -> DIFFERENT (Change detected)")
    else:
        # Check content if size is same (unlikely for processed image but possible)
        with open(inp, 'rb') as f1, open(out, 'rb') as f2:
            if f1.read() != f2.read():
                print(f"  -> DIFFERENT (Content changed)")
            else:
                print(f"  -> IDENTICAL (No change)")
