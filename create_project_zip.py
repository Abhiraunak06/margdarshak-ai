import os
import zipfile

def make_zip():
    root_dir = r'C:\jee'
    zip_path = r'C:\jee\careerpath-ai-platform.zip'
    
    ignore_dirs = {
        'node_modules', '.git', '__pycache__', '.pytest_cache', 
        '.venv', 'venv', 'dist', '.idea', '.vscode'
    }
    ignore_files = {'careerpath-ai-platform.zip', 'create_project_zip.py'}
    
    print(f'Creating zip archive: {zip_path}')
    total_files = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(root_dir):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for f in files:
                if f in ignore_files or f.endswith('.pyc'):
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, root_dir)
                zf.write(full_path, rel_path)
                total_files += 1

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f'Archive created successfully! Total files: {total_files}, Size: {size_mb:.2f} MB')

if __name__ == '__main__':
    make_zip()
