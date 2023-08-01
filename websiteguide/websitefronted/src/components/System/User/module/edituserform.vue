<template>
  <Modal
    v-model="modal"
    title="Редактировать пользователя"
    :closable="false"
    footer-hide>
    <Form ref="form" :model="form" :label-width="120" :rules="rules">
      <FormItem label="Имя пользователя" prop="username">
        <Input type="text" autoComplete="off" v-model="form.username" clearable placeholder="Введите имя пользователя"
               style="width: 300px;"></Input>
      </FormItem>
      <FormItem label="Имя" prop="alias">
        <Input type="text" v-model="form.alias" clearable placeholder="Введите имя"
               style="width: 300px;"></Input>
      </FormItem>
      <FormItem>
        <Row>
          <Col span="4" offset="14">
            <Button type="primary" @click="handleSubmit('form')">ОК</Button>
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
        name: "edituserform",
        data() {
            return {
                rowId: null,
                modal: false,
                form: {
                    username: '',
                    alias: '',
                },
                rules: {
                    username: {required: true, message: 'Имя пользователя не может быть пустым', trigger: 'blur'},
                    alias: {required: true, message: 'Имя не может быть пустым', trigger: 'blur'},
                }
            }
        },
        mounted() {
        },
        methods: {
            handleSubmit() {
                axios.patch(`api/user/${this.rowId}/`, this.form).then(resp => {
                    this.modal = false
                    this.$Message.success('Успешно отредактировано')
                    this.$parent.init()
                }).catch(error => {
                    this.$Notice.error({
                        title: 'Ошибка редактирования',
                        desc: JSON.stringify(error.response.data)
                    })
                })
            },
            handleCancel(name) {
                this.modal = false
                this.$refs[name].resetFields()
                this.form = {
                    username: '',
                    alias: '',
                }
            }
        }
    }
</script>

<style scoped>

</style>
