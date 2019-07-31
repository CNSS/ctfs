<template>
  <el-card class="box-card" style="text-align: center">
    <el-upload
      action=""
      class="upload-demo"
      drag
      :http-request="upload"
      :beforeUpload="beforeAvatarUpload">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
    </el-upload>
  </el-card>
</template>

<script>
import { upload } from '@/util/api'
export default {
  name: 'Index',
  data () {
    return {
    }
  },
  methods: {
    upload (param) {
      upload(this, param.file, (response) => {
        this.$alert('<div style="word-break:break-all;">下载地址：<code>/api/upload?token=' + response.body.data.token + '</code></div>', '上传成功', {
          confirmButtonText: '确定',
          dangerouslyUseHTMLString: true
        })
      }, (response) => {
        if (response.status === 502) {
          this.$alert('后端还未启动好所有服务，请耐心等待...', '上传失败', {
            confirmButtonText: '确定'
          })
          return
        }
        this.$alert('上传失败了呢...', '上传失败', {
          confirmButtonText: '确定'
        })
      })
    },
    beforeAvatarUpload (file) {
      const fileSizeLimit = file.size / 1024 / 1024 < 10
      if (!fileSizeLimit) {
        this.$message({
          message: '上传文件大小不能超过 10MB!',
          type: 'warning'
        })
      }
      return fileSizeLimit
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
