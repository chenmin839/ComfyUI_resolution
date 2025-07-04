# ComfyUI 图像比例选择插件
B站--专横的佩奇
一个专为ComfyUI设计的分辨率选择插件
## 🎯 核心特点
- 🟢 **绿色分类标题**: 清晰的视觉分隔，快速定位所需分辨率类型
- 🎯 **智能预设选择**: 无需记忆复杂数字，直观的分辨率描述
- 📱 **全面设备支持**: 从iPhone 2G到iPhone 16 Pro Max全系列覆盖
- 🔄 **双模式切换**: 预设分辨率与自定义尺寸无缝切换
- 🖼️ **AI模型优化**: 专门为SD 1.5和SDXL优化的分辨率预设
- 📺 **多场景覆盖**: 社交媒体、视频制作、桌面应用等全场景
- ✅ **VAE完美兼容**: 自动确保所有分辨率都是8的倍数
- 🎬 **专业标准**: 严格按照行业标准和设备官方规格设计

## 🚀 安装方法

1. **下载插件**
   ```bash
   cd ComfyUI/custom_nodes/
   git clone [项目地址]
   ```

2. **重启ComfyUI**
   - 重启ComfyUI应用程序

3. **找到节点**
   - 在节点菜单中：`右键` → `latent` → `Cm Latent Image`

## 📱 使用指南

### 基本操作
1. 在ComfyUI工作流中添加 **Cm Latent Image** 节点
2. 选择模式：
   - **预设分辨率**: 从分类预设中选择
   - **自定义尺寸**: 手动输入宽度和高度
3. 从下拉菜单选择分辨率（绿色标题为分类，正常文本为具体分辨率）
4. 设置 `batch_size`（批处理数量）
5. 连接到KSampler或其他latent输入节点