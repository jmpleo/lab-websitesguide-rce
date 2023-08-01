<template>
  <Modal
    v-model="modal"
    title="Добавить пользователя"
    :closable="false"
    footer-hide>
    <Form ref="form" :model="form" :label-width="120" :rules="rules">
      <FormItem label="Имя пользователя" prop="username">
        <Input type="text" autoComplete="off" v-model="form.username" clearable placeholder="Введите имя пользователя"
               style="width: 300px;"></Input>
      </FormItem>
      <FormItem label="Имя" prop="alias">
        <Input type="text"  v-model="form.alias" clearable placeholder="Введите имя"
               style="width: 300px;"></Input>
      </FormItem>
      <FormItem label="Пароль" prop="password">
        <Input type="password" v-model="form.password" clearable placeholder="Введите пароль"
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
        name: "adduserform",
        data() {
            return {
                modal: false,
                form: {
                    username: '',
                    alias:'',
                    password:''
                },
                rules:{
                    username:{required:true,message:'Имя пользователя не может быть пустым',trigger:'blur'},
                    alias:{required:true,message:'Имя не может быть пустым',trigger:'blur'},
                    password:{required:true,message:'Пароль не может быть пустым',trigger:'blur'}
                }
            }
        },
        mounted(){
        },
        methods: {
            handleSubmit() {
                axios.post('api/user/',this.form).then(resp =>{
                    this.modal = false
                    this.$Message.success('Успешно добавлено')
                    this.$parent.init()
                }).catch(error =>{
                    this.$Notice.error({
                        title:'Ошибка добавления',
                        desc:JSON.stringify(error.response.data)
                    })
                })
            },
            handleCancel(name) {
                this.modal = false
                this.$refs[name].resetFields()
                this.form = {
                    username: '',
                    alias:'',
                    password: ''
                }
            }
        }
    }
</script>

<style scoped>

</style>
