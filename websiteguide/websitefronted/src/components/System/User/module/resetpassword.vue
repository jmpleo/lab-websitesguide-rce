<template>
  <Modal
    v-model="modal"
    title="Сброс пароля"
    :closable="false"
    footer-hide>
    <Form ref="form" :model="form" :label-width="120" :rules="rules">
      <FormItem label="Пароль" prop="password1">
        <Input type="password" v-model="form.password1" autocomplete="off" clearable placeholder="Введите пароль"
               style="width: 300px;"></Input>
      </FormItem>
      <FormItem label="Подтверждение пароля" prop="password2">
        <Input type="password" v-model="form.password2" autocomplete="off" clearable placeholder="Введите пароль"
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
        name: "resetpassword",
        data() {
            return {
                modal: false,
                rowId: null,
                form: {
                    password1: '',
                    password2: ''
                },
                rules: {
                    password1: {required: true, message: 'Пароль не может быть пустым', trigger: 'blur'},
                    password2: {required: true, message: 'Подтверждение пароля не может быть пустым', trigger: 'blur'}
                }
            }
        },
        methods: {
            handleSubmit() {
                axios.post(`api/user/${this.rowId}/change-passwd/`, this.form).then(resp => {
                    this.modal = false
                    this.form = {
                        password1: '',
                        password2: ''
                    }
                    this.$Message.success('Пароль успешно сброшен')
                    this.$parent.init()
                }).catch(error => {
                    this.$Notice.error({
                        title: 'Ошибка сброса пароля',
                        desc: JSON.stringify(error.response.data.msg)
                    })
                })
            },
            handleCancel(name) {
                this.modal = false
                this.$refs[name].resetFields()
                this.form = {
                    password1: '',
                    password2: ''
                }
            }
        }
    }
</script>

<style scoped>

</style>
