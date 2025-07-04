import torch

class AspectRatioLatentImage:
    """
    ComfyUI插件：图像比例选择器
    提供预设的图像分辨率选择，包括SD模型常用尺寸、电脑分辨率和移动设备分辨率
    同时支持用户自定义宽度和高度输入
    """
    
    def __init__(self):
        self.device = "cpu"

    @classmethod
    def INPUT_TYPES(s):
        # 预设分辨率列表，按分类组织
        resolution_presets = [
            # === AI图像生成专用分辨率 ===
            "🟢 === SD 1.5 分辨率 (512基础) ===",
            "512x512 (1:1) SD1.5 正方形",
            "512x768 (2:3) SD1.5 竖版",
            "768x512 (3:2) SD1.5 横版", 
            "512x704 (8:11) SD1.5 常用竖版",
            "704x512 (11:8) SD1.5 常用横版",
            "512x576 (8:9) SD1.5 中等竖版",
            "576x512 (9:8) SD1.5 中等横版",
            "512x896 (4:7) SD1.5 竖屏",
            "896x512 (7:4) SD1.5 横屏",
            "448x512 (7:8) SD1.5 窄竖版",
            "512x448 (8:7) SD1.5 宽横版",
            "640x512 (5:4) SD1.5 接近4:3",
            "512x640 (4:5) SD1.5 接近3:4",
            "384x512 (3:4) SD1.5 标准竖版",
            "512x384 (4:3) SD1.5 标准横版",
            "512x614 (5:6) SD1.5 接近正方形竖版",
            "614x512 (6:5) SD1.5 接近正方形横版",
            "768x768 (1:1) SD1.5 大正方形",
            
            "🟢 === SDXL 分辨率 (1024基础) ===",
            "1024x1024 (1:1) SDXL 正方形",
            "832x1216 (2:3) SDXL 竖版",
            "1216x832 (3:2) SDXL 横版",
            "1024x1280 (4:5) SDXL 标准竖版",
            "1280x1024 (5:4) SDXL 标准横版",
            "1024x1408 (8:11) SDXL 常用竖版",
            "1408x1024 (11:8) SDXL 常用横版",
            "768x1344 (4:7) SDXL 竖屏",
            "1344x768 (7:4) SDXL 横屏",
            "896x1152 (7:9) SDXL 竖版比例",
            "1152x896 (9:7) SDXL 横版比例",
            "896x1024 (7:8) SDXL 窄竖版",
            "1024x896 (8:7) SDXL 宽横版",
            "1024x1536 (2:3) SDXL 高竖版",
            "1536x1024 (3:2) SDXL 宽横版",
            
            # === 桌面电脑分辨率 ===
            "🟢 === 桌面电脑分辨率 ===",
            "1920x1080 (16:9) Full HD",
            "2560x1440 (16:9) 2K QHD",
            "3840x2160 (16:9) 4K UHD",
            "1366x768 (16:9) 笔记本最常见",
            "1280x720 (16:9) HD",
            "1600x900 (16:9) 宽屏",
            "1920x1200 (16:10) 专业显示器",
            "2560x1600 (16:10) 高端显示器",
            "1680x1050 (16:10) 中等分辨率",
            "3440x1440 (21:9) 超宽屏",
            "2560x1080 (21:9) 超宽游戏",
            "5120x2880 (16:9) 5K显示器",
            "1024x768 (4:3) 经典比例",
            "1280x1024 (5:4) 接近正方形",
            "1440x900 (8:5) Mac风格",
            "1200x1600 (3:4) 竖屏显示器",
            "1080x1920 (9:16) 竖屏显示器",
            
            # === 游戏常用分辨率 ===
            "🟢 === 游戏常用分辨率 ===",
            "1280x960 (4:3) CS经典",
            "1440x1080 (4:3) 拉伸4:3",
            "2048x1536 (4:3) iPad Pro分辨率",
            
            # === 艺术创作分辨率 ===
            "🟢 === 艺术创作分辨率 ===",
            "512x724 (√2:1) SD1.5 A4竖版",
            "724x512 (1:√2) SD1.5 A4横版",
            "1024x1448 (√2:1) SDXL A4竖版",
            "1448x1024 (1:√2) SDXL A4横版",
            "512x829 (φ:1) SD1.5 黄金竖版",
            "829x512 (1:φ) SD1.5 黄金横版",
            "1024x1658 (φ:1) SDXL 黄金竖版",
            "1658x1024 (1:φ) SDXL 黄金横版",
            "512x683 (3:4) SD1.5 经典竖版",
            "683x512 (4:3) SD1.5 经典横版",
            "1200x1800 (2:3) 印刷竖版",
            "1800x1200 (3:2) 印刷横版",
            
            # === 社交媒体分辨率 ===
            "🟢 === 社交媒体分辨率 ===",
            "1080x1080 (1:1) Instagram正方形",
            "1080x1350 (4:5) Instagram竖版",
            "1080x1920 (9:16) TikTok竖屏",
            "1920x1080 (16:9) YouTube横屏",
            
            # === 视频制作分辨率 ===
            "🟢 === 视频制作分辨率 ===",
            "1920x1080 (16:9) Full HD视频",
            "1280x720 (16:9) HD视频",
            "3840x2160 (16:9) 4K视频",
            "2560x1440 (16:9) 2K视频",
            "1280x1280 (1:1) 正方形视频",
            "720x1280 (9:16) 竖屏短视频",
            
            # === iPhone设备分辨率 ===
            "🟢 === iPhone早期系列 (2G-4s) ===",
            "320x480 (2:3) iPhone早期竖屏",
            "480x320 (3:2) iPhone早期横屏",
            "640x960 (2:3) iPhone4/4s竖屏", 
            "960x640 (3:2) iPhone4/4s横屏",
            
            "🟢 === iPhone 5系列 ===",
            "640x1136 (9:16) iPhone5系列竖屏",
            "1136x640 (16:9) iPhone5系列横屏",
            
            "🟢 === iPhone 6-8系列 ===",
            "752x1336 (9:16) iPhone6/7/8竖屏",
            "1336x752 (16:9) iPhone6/7/8横屏",
            "1080x1920 (9:16) iPhone6/7/8 Plus竖屏",
            "1920x1080 (16:9) iPhone6/7/8 Plus横屏",
            
            "🟢 === iPhone X系列 ===",
            "576x1248 (9:19.5) iPhoneX/XS竖屏缩放",
            "1248x576 (19.5:9) iPhoneX/XS横屏缩放",
            "832x1792 (9:19.5) iPhoneXR/11竖屏",
            "1792x832 (19.5:9) iPhoneXR/11横屏",
            
            "🟢 === iPhone 12系列 ===",
            "1080x2344 (9:19.5) iPhone12/13mini竖屏",
            "2344x1080 (19.5:9) iPhone12/13mini横屏",
            "1176x2536 (9:19.5) iPhone12/13/Pro竖屏",
            "2536x1176 (19.5:9) iPhone12/13/Pro横屏",
            "1288x2784 (9:19.5) iPhone12/13ProMax竖屏",
            "2784x1288 (19.5:9) iPhone12/13ProMax横屏",
            
            "🟢 === iPhone 14系列 ===",
            "1184x2560 (9:19.5) iPhone14/15竖屏",
            "2560x1184 (19.5:9) iPhone14/15横屏",
            "1296x2800 (9:19.5) iPhone14/15Plus竖屏",
            "2800x1296 (19.5:9) iPhone14/15Plus横屏",
            
            "🟢 === iPhone 16系列 ===",
            "1208x2624 (9:19.5) iPhone16Pro竖屏",
            "2624x1208 (19.5:9) iPhone16Pro横屏",
            "1320x2872 (9:19.5) iPhone16ProMax竖屏",
            "2872x1320 (19.5:9) iPhone16ProMax横屏",
            
            "🟢 === iPhone SE系列 ===",
            "640x1136 (9:16) iPhoneSE1竖屏",
            "1136x640 (16:9) iPhoneSE1横屏",
            "752x1336 (9:16) iPhoneSE2/3竖屏",
            "1336x752 (16:9) iPhoneSE2/3横屏",
        ]
        
        return {
            "required": {
                "mode": (["预设分辨率", "自定义尺寸"], {
                    "default": "预设分辨率"
                }),
                "resolution_preset": (resolution_presets, {
                    "default": "1024x1024 (1:1) SDXL 正方形"
                }),
                "width": ("INT", {
                    "default": 1024, 
                    "min": 64, 
                    "max": 8192, 
                    "step": 8
                }),
                "height": ("INT", {
                    "default": 1024, 
                    "min": 64, 
                    "max": 8192, 
                    "step": 8
                }),
                "batch_size": ("INT", {
                    "default": 1, 
                    "min": 1, 
                    "max": 4096
                }),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate"
    CATEGORY = "latent"

    def generate(self, mode, resolution_preset, width, height, batch_size=1):
        """
        根据选择的模式生成空的latent图像
        支持预设分辨率和自定义尺寸两种模式
        """
        if mode == "预设分辨率":
            # 检查是否选中了分类标题
            if resolution_preset.startswith("🟢 ==="):
                # 如果选中了分类标题，使用默认分辨率
                final_width, final_height = 1024, 1024
                print(f"警告: 选中了分类标题 '{resolution_preset}', 使用默认分辨率 1024x1024")
            else:
                # 使用预设分辨率模式
                try:
                    # 解析格式："1024x1024 (1:1) SDXL 正方形"
                    resolution_part = resolution_preset.split(' ')[0]  # 获取 "1024x1024"
                    final_width, final_height = map(int, resolution_part.split('x'))
                except (ValueError, IndexError):
                    # 如果解析失败，使用默认值
                    final_width, final_height = 1024, 1024
                    print(f"警告: 解析分辨率失败 '{resolution_preset}', 使用默认分辨率 1024x1024")
        else:
            # 使用自定义尺寸模式
            final_width, final_height = width, height
            
        # 确保尺寸是8的倍数（VAE要求）
        final_width = (final_width // 8) * 8
        final_height = (final_height // 8) * 8
        
        # 生成空的latent张量
        # Latent空间的尺寸是图像尺寸的1/8
        latent_width = final_width // 8
        latent_height = final_height // 8
        
        # 创建空的latent张量 [batch_size, channels, height, width]
        latent = torch.zeros([batch_size, 4, latent_height, latent_width])
        
        return ({"samples": latent}, )

    @classmethod
    def IS_CHANGED(s, mode, resolution_preset, width, height, batch_size):
        """
        当输入参数改变时重新生成
        """
        return f"{mode}_{resolution_preset}_{width}_{height}_{batch_size}" 