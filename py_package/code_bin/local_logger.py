from datetime import datetime
from pathlib import Path

class Logger(object):
    
    def __init__(self, log_dir: str):
        self.log_dir = log_dir  
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
    def get_qty_path(self):
        save_path = self.log_dir / 'quantity'
        save_path.mkdir(parents=True, exist_ok=True)
        save_path = save_path / datetime.now().strftime('%Y-%m-%d')
        save_path = save_path.as_posix() + '.txt'
        return save_path
        
    def get_img_path(self):
        save_path = self.log_dir / 'images'
        save_path = save_path / datetime.now().strftime('%Y-%m-%d')
        save_path.mkdir(parents=True, exist_ok=True)
        save_file = save_path / datetime.now().strftime('%H-%M-%S')
        save_file = save_file.as_posix() + '.jpg'
        return save_file
