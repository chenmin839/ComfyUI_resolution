"""
ComfyUI图像比例选择插件配置文件
包含所有预设分辨率和相关配置
"""

from typing import List, Dict, Any

# 版本信息
VERSION = "1.1.0"
PLUGIN_NAME = "ComfyUI Resolution Plugin"

# 预设分辨率配置
RESOLUTION_PRESETS: List[str] = [
    # SD 1.5 常用分辨率 (512基础)
    "512x512 (1:1) SD1.5 正方形",
    "512x768 (2:3) SD1.5 竖版",
    "768x512 (3:2) SD1.5 横版", 
    "512x896 (4:7) SD1.5 竖屏",
    "896x512 (7:4) SD1.5 横屏",
    "640x512 (5:4) SD1.5 接近4:3",
    "512x640 (4:5) SD1.5 接近3:4",
    "768x768 (1:1) SD1.5 大正方形",
    
    # SDXL 常用分辨率 (1024基础)
    "1024x1024 (1:1) SDXL 正方形",
    "832x1216 (2:3) SDXL 竖版",
    "1216x832 (3:2) SDXL 横版",
    "768x1344 (4:7) SDXL 竖屏",
    "1344x768 (7:4) SDXL 横屏",
    "896x1152 (7:9) SDXL iPhone比例",
    "1152x896 (9:7) SDXL iPhone横屏",
    "1024x1536 (2:3) SDXL 高竖版",
    "1536x1024 (3:2) SDXL 宽横版",
    
    # iPhone 设备分辨率 (适配SD)
    "480x320 (3:2) iPhone早期",
    "1136x640 (16:9) iPhone5系列",
    "1344x752 (16:9) iPhone6/7/8",
    "1024x472 (19.5:9) iPhoneX系列缩放",
    "2048x944 (19.5:9) iPhoneX高清",
    
    # 社交媒体常用
    "1080x1080 (1:1) Instagram正方形",
    "1080x1350 (4:5) Instagram竖版",
    "1920x1080 (16:9) YouTube横屏",
    "1080x1920 (9:16) TikTok竖屏",
    
    # 视频常用分辨率
    "1920x1080 (16:9) Full HD",
    "1280x720 (16:9) HD",
    "3840x2160 (16:9) 4K",
    "2560x1440 (16:9) 2K",
    
    # 其他常用比例
    "1024x768 (4:3) 经典比例",
    "1280x1024 (5:4) 接近正方形",
    "1600x900 (16:9) 宽屏",
    "1440x900 (8:5) Mac风格",
]

# 默认设置
DEFAULT_SETTINGS: Dict[str, Any] = {
    "default_preset": "1024x1024 (1:1) SDXL 正方形",
    "default_width": 1024,
    "default_height": 1024,
    "default_batch_size": 1,
    "min_resolution": 64,
    "max_resolution": 8192,
    "max_batch_size": 4096,
    "vae_divisor": 8,  # VAE要求尺寸必须是8的倍数
}

# 模式选项
MODE_OPTIONS: List[str] = ["预设分辨率", "自定义尺寸"]

# 分辨率分类（用于未来扩展）
RESOLUTION_CATEGORIES: Dict[str, List[str]] = {
    "SD1.5": [preset for preset in RESOLUTION_PRESETS if "SD1.5" in preset],
    "SDXL": [preset for preset in RESOLUTION_PRESETS if "SDXL" in preset],
    "iPhone": [preset for preset in RESOLUTION_PRESETS if "iPhone" in preset],
    "社交媒体": [preset for preset in RESOLUTION_PRESETS if any(platform in preset for platform in ["Instagram", "YouTube", "TikTok"])],
    "视频": [preset for preset in RESOLUTION_PRESETS if any(res in preset for res in ["HD", "4K", "2K"])],
} 