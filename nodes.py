"""
ComfyUI图像比例选择插件 - 主节点文件
优化版本：添加类型提示，使用配置文件，改进错误处理
"""

import torch
from typing import Tuple, Dict, Any, Optional
from functools import lru_cache
import logging

from .config import (
    RESOLUTION_PRESETS, 
    DEFAULT_SETTINGS, 
    MODE_OPTIONS,
    VERSION
)

# 配置日志
logger = logging.getLogger(__name__)

class ResolutionUtils:
    """分辨率处理工具类"""
    
    @staticmethod
    @lru_cache(maxsize=128)
    def parse_resolution_preset(preset: str) -> Tuple[int, int]:
        """
        解析预设分辨率字符串
        
        Args:
            preset: 格式如 "1024x1024 (1:1) SDXL 正方形"
            
        Returns:
            Tuple[int, int]: (宽度, 高度)
            
        Raises:
            ValueError: 解析失败时抛出异常
        """
        try:
            # 提取分辨率部分："1024x1024"
            resolution_part = preset.split(' ')[0]
            width_str, height_str = resolution_part.split('x')
            width, height = int(width_str), int(height_str)
            
            if width <= 0 or height <= 0:
                raise ValueError(f"无效的分辨率值: {width}x{height}")
                
            return width, height
            
        except (ValueError, IndexError) as e:
            logger.error(f"解析分辨率预设失败: {preset}, 错误: {e}")
            raise ValueError(f"无法解析分辨率预设: {preset}")
    
    @staticmethod
    def ensure_vae_compatible(width: int, height: int, divisor: int = 8) -> Tuple[int, int]:
        """
        确保尺寸符合VAE要求（8的倍数）
        
        Args:
            width: 原始宽度
            height: 原始高度
            divisor: 除数，默认为8
            
        Returns:
            Tuple[int, int]: 调整后的(宽度, 高度)
        """
        adjusted_width = (width // divisor) * divisor
        adjusted_height = (height // divisor) * divisor
        
        # 确保不为0
        adjusted_width = max(adjusted_width, divisor)
        adjusted_height = max(adjusted_height, divisor)
        
        if adjusted_width != width or adjusted_height != height:
            logger.info(f"尺寸已调整为VAE兼容: {width}x{height} -> {adjusted_width}x{adjusted_height}")
            
        return adjusted_width, adjusted_height
    
    @staticmethod
    def create_latent_tensor(batch_size: int, width: int, height: int) -> torch.Tensor:
        """
        创建latent张量
        
        Args:
            batch_size: 批次大小
            width: 图像宽度
            height: 图像高度
            
        Returns:
            torch.Tensor: latent张量
        """
        # Latent空间的尺寸是图像尺寸的1/8
        latent_width = width // 8
        latent_height = height // 8
        
        # 创建空的latent张量 [batch_size, channels, height, width]
        return torch.zeros([batch_size, 4, latent_height, latent_width])


class AspectRatioLatentImage:
    """
    ComfyUI插件：图像比例选择器 (优化版)
    提供预设的图像分辨率选择，包括iPhone设备分辨率和SD模型常用尺寸
    同时支持用户自定义宽度和高度输入
    """
    
    def __init__(self) -> None:
        self.device: str = "cpu"
        self.version: str = VERSION
        logger.info(f"AspectRatioLatentImage 初始化完成 - 版本: {VERSION}")

    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        """定义输入类型"""
        return {
            "required": {
                "mode": (MODE_OPTIONS, {
                    "default": MODE_OPTIONS[0]
                }),
                "resolution_preset": (RESOLUTION_PRESETS, {
                    "default": DEFAULT_SETTINGS["default_preset"]
                }),
                "width": ("INT", {
                    "default": DEFAULT_SETTINGS["default_width"], 
                    "min": DEFAULT_SETTINGS["min_resolution"], 
                    "max": DEFAULT_SETTINGS["max_resolution"], 
                    "step": DEFAULT_SETTINGS["vae_divisor"]
                }),
                "height": ("INT", {
                    "default": DEFAULT_SETTINGS["default_height"], 
                    "min": DEFAULT_SETTINGS["min_resolution"], 
                    "max": DEFAULT_SETTINGS["max_resolution"], 
                    "step": DEFAULT_SETTINGS["vae_divisor"]
                }),
                "batch_size": ("INT", {
                    "default": DEFAULT_SETTINGS["default_batch_size"], 
                    "min": 1, 
                    "max": DEFAULT_SETTINGS["max_batch_size"]
                }),
            }
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate"
    CATEGORY = "latent"

    def _get_resolution_from_mode(self, mode: str, resolution_preset: str, 
                                  width: int, height: int) -> Tuple[int, int]:
        """
        根据模式获取分辨率
        
        Args:
            mode: 模式选择
            resolution_preset: 预设分辨率
            width: 自定义宽度
            height: 自定义高度
            
        Returns:
            Tuple[int, int]: (最终宽度, 最终高度)
        """
        if mode == "预设分辨率":
            try:
                return ResolutionUtils.parse_resolution_preset(resolution_preset)
            except ValueError as e:
                logger.warning(f"使用预设分辨率失败，回退到默认值: {e}")
                return (DEFAULT_SETTINGS["default_width"], DEFAULT_SETTINGS["default_height"])
        else:
            # 自定义尺寸模式
            return width, height

    def generate(self, mode: str, resolution_preset: str, width: int, 
                height: int, batch_size: int = 1) -> Tuple[Dict[str, torch.Tensor]]:
        """
        根据选择的模式生成空的latent图像
        
        Args:
            mode: 模式选择 ("预设分辨率" 或 "自定义尺寸")
            resolution_preset: 预设分辨率字符串
            width: 自定义宽度
            height: 自定义高度
            batch_size: 批次大小
            
        Returns:
            Tuple[Dict[str, torch.Tensor]]: 包含latent张量的字典
        """
        try:
            # 获取分辨率
            final_width, final_height = self._get_resolution_from_mode(
                mode, resolution_preset, width, height
            )
            
            # 确保VAE兼容性
            final_width, final_height = ResolutionUtils.ensure_vae_compatible(
                final_width, final_height, DEFAULT_SETTINGS["vae_divisor"]
            )
            
            # 创建latent张量
            latent = ResolutionUtils.create_latent_tensor(
                batch_size, final_width, final_height
            )
            
            logger.info(f"生成latent成功: {final_width}x{final_height}, batch_size={batch_size}")
            
            return ({"samples": latent},)
            
        except Exception as e:
            logger.error(f"生成latent失败: {e}")
            # 使用默认设置作为后备方案
            default_width = DEFAULT_SETTINGS["default_width"]
            default_height = DEFAULT_SETTINGS["default_height"]
            latent = ResolutionUtils.create_latent_tensor(batch_size, default_width, default_height)
            logger.info(f"使用默认设置生成latent: {default_width}x{default_height}")
            return ({"samples": latent},)

    @classmethod
    def IS_CHANGED(cls, mode: str, resolution_preset: str, width: int, 
                   height: int, batch_size: int) -> str:
        """
        当输入参数改变时重新生成
        
        Args:
            mode: 模式选择
            resolution_preset: 预设分辨率
            width: 宽度
            height: 高度
            batch_size: 批次大小
            
        Returns:
            str: 参数的哈希值，用于检测变化
        """
        return f"{mode}_{resolution_preset}_{width}_{height}_{batch_size}"

    def get_info(self) -> Dict[str, Any]:
        """
        获取节点信息
        
        Returns:
            Dict[str, Any]: 节点信息
        """
        return {
            "name": "AspectRatioLatentImage",
            "version": self.version,
            "description": "图像比例选择器 - 提供预设分辨率和自定义尺寸选择",
            "presets_count": len(RESOLUTION_PRESETS),
            "categories": list(RESOLUTION_PRESETS),
        } 