import zipfile
import os

def zip_project(output_filename):
    exclude_dirs = {'.git', '.github', 'temp_uploads', '__pycache__', 'build', 'out', 'vcpkg_installed'}
    exclude_files = {'GeminiWatermarkTool-Windows-x64.zip', 'fetch_links.py', 'download_and_extract.py', 'check_dims.py', 'split_image.py', 'compare_results.py', 'compare_restoration.py', 'verify_user_image.py', 'verify_user_image_2.py', 'zip_project.py'}
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files:
                    continue
                if file.endswith('.zip') and file != output_filename: # Avoid zipping other zips
                    continue
                    
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, '.')
                print(f"Adding {arcname}")
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    zip_project("GeminiWatermarkTool_Project.zip")
    print("Project zipped successfully.")
