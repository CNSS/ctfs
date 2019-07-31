const API_BASE = '/api'

export function upload (context, file, successCallback, failCallback) {
  const loading = context.$loading({
    lock: true,
    text: '上传中...',
    spinner: 'el-icon-loading',
    background: 'rgba(0, 0, 0, 0.7)'
  })
  let formData = new FormData()
  formData.append('file', file)
  context.$http.post(API_BASE + '/upload',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
  ).then(response => {
    loading.close()
    successCallback(response)
  }).catch(response => {
    loading.close()
    failCallback(response)
  })
}

export function getFileList (context, successCallback, failCallback) {
  context.$http.get(API_BASE + '/upload/list'
  ).then(response => {
    successCallback(response)
  }).catch(response => {
    failCallback(response)
  })
}
