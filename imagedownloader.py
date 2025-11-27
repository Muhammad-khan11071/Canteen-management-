import os
import shutil
import pandas as pd
import sys
from types import ModuleType

# ==========================================
# 🔧 PYTHON 3.13 FIX
# ==========================================
try:
    import imghdr
except ImportError:
    fake_imghdr = ModuleType("imghdr")
    def what(file, h=None):
        return 'jpeg'
    fake_imghdr.what = what
    sys.modules["imghdr"] = fake_imghdr
# ==========================================

from icrawler.builtin import BingImageCrawler

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, 'master_menu.csv')
FINAL_IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'images')
TEMP_DOWNLOAD_DIR = os.path.join(BASE_DIR, 'temp_images')

if not os.path.exists(FINAL_IMAGES_DIR):
    os.makedirs(FINAL_IMAGES_DIR)

def automate_downloads():
    print(f"Reading Menu from: {CSV_FILE}")
    
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"Loaded {len(df)} items.")
    except FileNotFoundError:
        print("[ERROR] master_menu.csv not found!")
        return

    for index, row in df.iterrows():
        item_id = str(row['id'])
        item_name = row['item']
        
        final_filename = f"{item_id}.jpeg"
        final_path = os.path.join(FINAL_IMAGES_DIR, final_filename)

        if os.path.exists(final_path):
            print(f"[SKIP] ID {item_id} ({item_name}) already exists.")
            continue

        print(f"\nDownloading ID {item_id}: {item_name}...", end=" ")

        crawler = BingImageCrawler(
            storage={'root_dir': TEMP_DOWNLOAD_DIR},
            log_level='CRITICAL'
        )

        # Search query
        crawler.crawl(keyword=f"{item_name} food", max_num=1)

        if os.path.exists(TEMP_DOWNLOAD_DIR):
            downloaded_files = os.listdir(TEMP_DOWNLOAD_DIR)
            
            if downloaded_files:
                src_file = os.path.join(TEMP_DOWNLOAD_DIR, downloaded_files[0])
                shutil.move(src_file, final_path)
                print("[DONE]")
            else:
                print("[NO IMAGE FOUND]")
            
            shutil.rmtree(TEMP_DOWNLOAD_DIR)
        else:
            print("[DOWNLOAD FAILED]")

    print("\n--- All Downloads Complete! ---")
    if os.path.exists(TEMP_DOWNLOAD_DIR):
        shutil.rmtree(TEMP_DOWNLOAD_DIR)

if __name__ == "__main__":
    automate_downloads()