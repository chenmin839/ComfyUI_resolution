# ComfyUI 图像比例选择插件 - 安装指南

## 快速安装

### 方法一：直接复制文件
1. 下载或克隆这个插件到本地
2. 将整个插件文件夹复制到 `ComfyUI/custom_nodes/` 目录下
3. 重启ComfyUI
4. 在节点菜单中找到新的节点

### 方法二：使用ComfyUI Manager
1. 在ComfyUI中打开Manager
2. 点击"Install via Git URL"
3. 输入这个插件的Git地址
4. 等待安装完成并重启

## 文件结构

安装后的文件结构应该如下：
```
ComfyUI/
└── custom_nodes/
    └── ComfyUI-AspectRatio-Plugin/
        ├── __init__.py          # 节点注册
        ├── nodes.py             # 主节点实现 (优化版)
        ├── config.py            # 配置文件 (新增)
        ├── README.md           # 项目说明
        ├── INSTALL.md          # 安装指南
        └── example_workflow.json # 示例工作流
```

## 节点说明

### 🎯 Cm Latent Image (AspectRatioLatentImage)
- **位置**: `latent` → `Cm Latent Image`
- **功能**: 
  - 预设分辨率选择（40+常用分辨率）
  - 自定义尺寸输入
  - 双模式支持：预设/自定义
- **特点**:
  - 类型安全的Python实现
  - 智能错误处理和回退机制
  - 自动VAE兼容性检查
  - 性能优化（LRU缓存）

## 使用示例

### 基础用法 - 预设分辨率
1. 添加 `Cm Latent Image` 节点
2. 选择模式："预设分辨率"
3. 从下拉菜单选择所需分辨率（如："1024x1024 (1:1) SDXL 正方形"）
4. 设置batch_size
5. 连接到KSampler的latent_image输入

### 自定义尺寸用法
1. 添加 `Cm Latent Image` 节点
2. 选择模式："自定义尺寸"
3. 输入自定义的宽度和高度
4. 系统自动调整为8的倍数（VAE兼容）
5. 连接到后续节点

### 预设分辨率分类

**SD 1.5 分辨率** (适合SD1.5模型):
- 512x512, 512x768, 768x512 等

**SDXL 分辨率** (适合SDXL模型):
- 1024x1024, 832x1216, 1216x832 等

**特殊用途分辨率**:
- iPhone系列：适配iPhone屏幕比例
- 社交媒体：Instagram、YouTube、TikTok格式
- 视频制作：HD、Full HD、4K标准

## 配置文件说明

### config.py 配置选项

您可以编辑 `config.py` 文件来自定义插件行为：

```python
# 添加新的预设分辨率
RESOLUTION_PRESETS.append("您的自定义分辨率")

# 修改默认设置
DEFAULT_SETTINGS["default_preset"] = "您喜欢的默认分辨率"
DEFAULT_SETTINGS["default_width"] = 512  # 自定义默认宽度
```

## 故障排除

### 常见问题

**Q: 安装后找不到节点**
A: 
- 确认文件复制到正确位置：`ComfyUI/custom_nodes/ComfyUI-AspectRatio-Plugin/`
- 重启ComfyUI
- 检查控制台是否有错误信息

**Q: 节点显示错误**
A:
- 确认ComfyUI版本是否支持（建议最新版本）
- 检查Python版本（建议3.8+）
- 查看ComfyUI控制台的详细错误日志

**Q: 分辨率计算不正确**
A:
- 所有分辨率都会自动调整为8的倍数（VAE技术要求）
- 这是正常现象，不是bug
- 如果输入1023x1023，会自动调整为1024x1024

**Q: 自定义分辨率不生效**
A:
- 确保选择了"自定义尺寸"模式
- 检查输入的数值是否在有效范围内(64-8192)
- 系统会自动调整为8的倍数

### 依赖要求

本插件依赖以下组件（通常ComfyUI已包含）：
- Python 3.8+
- PyTorch
- ComfyUI核心
- typing模块（Python内置）

### 兼容性

- ✅ ComfyUI最新版本
- ✅ Windows/Linux/macOS
- ✅ SD 1.5模型
- ✅ SDXL模型
- ✅ 其他自定义模型
- ✅ Python 3.8+ 类型提示支持

## 性能优化

### 缓存机制
- 插件使用LRU缓存来存储解析过的分辨率
- 重复使用相同预设时性能更佳
- 缓存大小：128个条目

### 内存使用
- 插件本身占用内存极少
- 只在生成latent时分配tensor内存
- 支持大批次处理（1-4096）

## 更新插件

### Git更新
如果使用Git安装：
```bash
cd ComfyUI/custom_nodes/ComfyUI-AspectRatio-Plugin
git pull origin main
```

### 手动更新
1. 备份当前的 `config.py`（如有自定义修改）
2. 下载新版本
3. 替换旧文件（保留自定义配置）
4. 重启ComfyUI

## 卸载插件

1. 删除 `ComfyUI/custom_nodes/ComfyUI-AspectRatio-Plugin` 文件夹
2. 重启ComfyUI
3. 节点将从菜单中消失

## 自定义配置

### 添加新的预设分辨率

编辑 `config.py` 文件：
```python
RESOLUTION_PRESETS.append("2048x2048 (1:1) 超高清正方形")
RESOLUTION_PRESETS.append("1920x800 (2.4:1) 电影比例")
```

### 修改默认设置

```python
DEFAULT_SETTINGS["default_preset"] = "512x512 (1:1) SD1.5 正方形"
DEFAULT_SETTINGS["max_batch_size"] = 8192  # 增加最大批次
```

## 开发者信息

- **版本**: v1.1.0
- **最后更新**: 2025年1月
- **代码特点**: 类型安全、错误处理、性能优化
- **Python要求**: 3.8+ (类型提示支持)

## 获取帮助

- 查看README.md了解功能详情
- 检查example_workflow.json示例工作流
- 在GitHub Issues页面报告问题
- 加入ComfyUI社区讨论

---

**祝您使用愉快！如有问题请及时反馈。** 