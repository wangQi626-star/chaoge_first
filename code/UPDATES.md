# 项目更新说明

## 新增功能

### 1. 模板系统增强
- 添加配色方案支持（color_scheme）
- 模板分类（经典、现代、创意、简约、多彩）
- 支持用户自定义模板
- 模板创建者追踪

### 2. 数据统计功能
- 用户简历统计页面
- 模板使用统计
- 热门模板 TOP 5 展示
- 可视化数据展示

### 3. 热门推荐系统
- 左侧推荐栏显示热门模板
- 基于使用次数的智能推荐
- 实时更新推荐列表

### 4. 简历分享功能
- 生成唯一分享链接
- 支持邮箱分享
- 支持微信分享
- 支持 QQ 分享
- 分享次数统计

## 数据库变更

### Resume 模型新增字段
- `share_token`: 分享令牌
- `share_count`: 分享次数
- `view_count`: 浏览次数

### ResumeTemplate 模型新增字段
- `color_scheme`: 配色方案（JSON）
- `category`: 模板分类
- `is_custom`: 是否自定义模板
- `creator`: 创建者（外键）

## API 新增接口

### 简历相关
- `POST /api/resumes/{id}/share/` - 生成分享链接
- `GET /api/resumes/statistics/` - 用户简历统计

### 模板相关
- `GET /api/templates/popular/` - 热门模板推荐
- `GET /api/templates/statistics/` - 模板统计数据
- `POST /api/templates/` - 创建自定义模板

## 前端新增页面

1. **Statistics.vue** - 数据统计页面
2. **TemplateEditor.vue** - 自定义模板编辑器
3. **ShareDialog.vue** - 分享对话框组件
4. **PopularSidebar.vue** - 热门推荐侧边栏

## 使用说明

### 运行迁移
```bash
cd backend
python manage.py migrate
```

### 访问新功能
- 统计页面: `/statistics`
- 模板编辑器: `/template-editor`
- 分享功能: 在历史记录页面点击"分享"按钮
