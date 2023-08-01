<template>
  <Modal
    v-model="modal"
    title="Замена логотипа"
    @on-ok="uploadIcon"
    @on-cancel="cancel">
    <div>
      <Upload
        ref="upload"
        :before-upload="handleUpload"
        action="">
        <Button icon="ios-cloud-upload-outline">Загрузить логотип</Button>
      </Upload>
      <div v-if="file !== null">Загруженный файл: {{ file.name }}
      </div>
    </div>
  </Modal>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "editIcon",
        props: {
            rowData: {
                type: Object,
                required: true
            }
        },
        data() {
            return {
                modal: false,
                file: null,
            }
        },

        methods: {
            handleUpload(file) {
                this.file = file;
                return false;
            },
            uploadIcon() {
                if (this.file == null) {
                    this.$Message.warning('Сначала загрузите файл')
                } else {
                    let data = new FormData();
                    data.append('id', this.rowData.id)
                    data.append('name', this.file.name)
                    data.append('file', this.file)
                    axios({
                        method: 'post',
                        url: `api/icon/`,
                        data: data,
                    }).then(resp => {
                        this.file = null
                        if (resp.data.code > 200) {
                            this.$Message.error(resp.data.msg)
                        } else {
                            this.$Message.success("Успешно заменено")
                        }
                    }).catch(error => {
                        console.log(error)
                        this.$Message.error("Не удалось заменить логотип")
                    })
                }

            },
            cancel() {
                this.file = null
            }
        }
    }
</script>

<style scoped>

</style>
