<template>
  <el-dialog v-model="visible" title="分享简历" width="500px">
    <div class="share-content">
      <el-input :model-value="shareUrl" readonly>
        <template #append>
          <el-button @click="copyUrl">复制</el-button>
        </template>
      </el-input>

      <el-divider />

      <div class="share-methods">
        <el-button @click="shareByWeChat" type="success">
          <el-icon><ChatDotRound /></el-icon> 微信分享
        </el-button>
        <el-button @click="shareByQQ" type="warning">
          <el-icon><ChatLineRound /></el-icon> QQ分享
        </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Message, ChatDotRound, ChatLineRound } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: Boolean,
  shareUrl: String
})

const emit = defineEmits(['update:modelValue'])

const visible = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const copyUrl = () => {
  navigator.clipboard.writeText(props.shareUrl)
  ElMessage.success('链接已复制')
}

const shareByEmail = () => {
  window.location.href = `mailto:?subject=我的简历&body=${props.shareUrl}`
}

const shareByWeChat = () => {
  ElMessage.info('请复制链接后在微信中分享')
  copyUrl()
}

const shareByQQ = () => {
  window.open(`https://connect.qq.com/widget/shareqq/index.html?url=${encodeURIComponent(props.shareUrl)}`)
}
</script>

<style scoped>
.share-content {
  padding: 20px 0;
}

.share-methods {
  display: flex;
  gap: 10px;
  justify-content: center;
}
</style>
