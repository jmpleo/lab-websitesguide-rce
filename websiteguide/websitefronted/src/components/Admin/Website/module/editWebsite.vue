<template>
  <Modal
    v-model="modal"
    :title="this.rowData.title"
    footer-hide>
    <Form ref="form" :model="form" :label-width="120" :rules="rules">
      <FormItem label="Заголовок" prop="title" @keydown.native.enter.prevent="()=>{}">
        <Input ref="InputGroup" type="text" v-model="form.title" clearable placeholder="Введите заголовок"
               style="width: 300px;"></Input>
      </FormItem>
      <FormItem label="URL" prop="path" @keydown.native.enter.prevent="()=>{}">
        <Input ref="InputGroup" type="text" v-model="form.path" clearable placeholder="Введите URL"
               style="width: 300px;"></Input>
      </FormItem>
      <FormItem label="Описание" prop="description" @keydown.native.enter.prevent="()=>{}">
        <Input ref="InputGroup" type="text" v-model="form.description" clearable placeholder="Введите описание"
               style="width: 300px;"></Input>
      </FormItem>
      <FormItem>
        <Row>
          <Col span="4" offset="14">
            <Button type="primary" @click="handleSubmit('form')">Сохранить</Button>
          </Col>
          <Col span="4">
            <Button type="error" @click="handleCancel('form')" style="margin-left: 8px">Отмена</Button>
          </Col>
        </Row>
      </FormItem>
    </Form>
  </Modal>
</template>

<script>
    import axios from 'axios'
    export default {
        name: "editWebsite",
        props: {
            rowData: {
                type: Object,
                required: true
            }
        },
        data() {
            return {
                modal: false,
                form: {
                    title: '',
                    path: '',
                    description: ''
                },
                rules: {
                    title: {
                        required: true, message: 'Заголовок не может быть пустым', trigger: 'blur'
                    },
                    path: {
                        required: true, message: 'URL не может быть пустым', trigger: 'blur'
                    },
                    description: {}
                }
            }
        },
        methods: {
            handleSubmit(name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        axios.patch(`api/website/${this.rowData.id}/`, this.form).then(resp => {
                            this.$Message.success('Успешно сохранено');
                            this.handleCancel(name)
                            this.$parent.refresh()
                        }).catch(error => {
                            this.$Message.err('Не удалось сохранить' + error)
                        })

                    }
                })
            },
            handleCancel(name) {
                this.modal = false
                this.$refs[name].resetFields()
            }
        }
    }
</script>

<style scoped>

</style>
