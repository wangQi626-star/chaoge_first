<template>
  <div class="popular-sidebar">
    <div class="sidebar-header">
      <h3>🔥 热门推荐</h3>
    </div>

    <div class="template-list">
      <div
        v-for="template in popularTemplates"
        :key="template.id"
        class="template-item"
        @click="selectTemplate(template.id)"
      >
        <div class="thumb-skeleton">
          <span class="thumb-id">#{{ template.id }}</span>
        </div>

        <div class="template-info">
          <div class="template-name" :title="template.name">{{ template.name }}</div>
          <div class="template-usage">已使用 {{ template.usage_count || 0 }} 次</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const popularTemplates = ref([])
// 👇 声明向父组件发送信号的事件
const emit = defineEmits(['select'])

const fetchPopular = async () => {
  try {
    const res = await api.get('/templates/popular/')
    popularTemplates.value = res.data || res
  } catch (error) {
    console.error('获取热门模板失败', error)
  }
}

const selectTemplate = (id) => {
  // 👇 点击时，不跳转页面了，而是把 id 发送给外面的主页面
  emit('select', id)
}

onMounted(() => {
  fetchPopular()
})
</script>
<style scoped>
/* 核心容器：防御一切塌陷和全局样式污染 */
.popular-sidebar {
  width: 100%;
  min-width: 240px; /* 强制兜底宽度，绝不变成面条 */
  box-sizing: border-box;
  padding: 24px 20px;
  background: #ffffff; /* 强制纯白底色 */
  border-radius: 20px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}

.sidebar-header {
  margin-bottom: 20px;
  border-bottom: 2px solid #f3f4f6;
  padding-bottom: 12px;
}

h3 {
  margin: 0;
  color: #0f172a;
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  writing-mode: horizontal-tb; /* 强制横排文字 */
}

.template-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.template-item {
  display: flex;
  flex-direction: row; /* 强制子元素左右横排 */
  align-items: center;
  gap: 14px;
  padding: 10px;
  border-radius: 12px;
  cursor: pointer;
  background: #f8fafc;
  border: 1px solid transparent;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.template-item:hover {
  background: #eff6ff;
  border-color: #bfdbfe;
  transform: translateX(6px); /* 鼠标悬浮时向右轻微移动交互 */
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
}

.thumb-skeleton {
  width: 48px;
  height: 64px;
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0; /* 核心：严禁图片/占位框被挤扁 */
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.6);
}

.thumb-id {
  font-size: 13px;
  color: #4f46e5;
  font-weight: 800;
}

.template-info {
  flex: 1;
  min-width: 0; /* 核心：允许文字超出时被隐藏而不是撑爆容器 */
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.template-name {
  font-weight: 600;
  color: #334155;
  font-size: 14px;
  /* 核心：防面条三连杀（不换行、超长隐藏、显示省略号） */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  writing-mode: horizontal-tb;
}

.template-usage {
  font-size: 12px;
  color: #94a3b8;
  writing-mode: horizontal-tb;
}
</style>