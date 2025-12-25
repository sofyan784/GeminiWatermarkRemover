import os

input_path = "C:/Users/Admin/.gemini/antigravity/brain/5b1cec57-710b-4e26-b8fc-7bebdd5c5483/uploaded_image_1766484250892.jpg"
output_path = "C:/Users/Admin/.gemini/antigravity/brain/5b1cec57-710b-4e26-b8fc-7bebdd5c5483/cleaned_image.jpg"

if os.path.exists(output_path):
    s_in = os.path.getsize(input_path)
    s_out = os.path.getsize(output_path)
    print(f"Input size: {s_in}")
    print(f"Output size: {s_out}")
    if s_in != s_out:
        print("Success: Output file created and size differs.")
    else:
        # Check content
        with open(input_path, 'rb') as f1, open(output_path, 'rb') as f2:
            if f1.read() != f2.read():
                print("Success: Output file created and content differs.")
            else:
                print("Warning: Output file identical to input.")
else:
    print("Error: Output file not found.")
