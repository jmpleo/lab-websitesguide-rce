<template>
  <div class="container">
    <Content :style="{padding: '0 30px'}">
      <Card dis-hover>
        <Row>
          <div>Сменить пароль</div>
        </Row>
        <div :style="{padding:'10px 0'}">
          <Form ref="form" :model="form" :label-width="120" :rules="rules">
            <FormItem label="Новый пароль" prop="password1">
              <Input type="password" v-model="form.password1" autocomplete="off" password placeholder="password"
                     style="width: 300px;"></Input>
            </FormItem>
            <FormItem label="Подтвердите пароль" prop="password2">
              <Input type="password" v-model="form.password2" autocomplete="off" password placeholder="password"
                     style="width: 300px;"></Input>
            </FormItem>
            <FormItem>
              <Row>
                <Col span="4">
                  <Button type="primary" @click="handleSubmit('form')">Сохранить</Button>
                </Col>
              </Row>
            </FormItem>
          </Form>
        </div>
      </Card>
    </Content>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'Center',
  data() {
    return {
      form: {
        password1: '',
        password2: ''
      },
      rules: {
        password1: {required: true, message: '', trigger: 'blur'},
        password2: {required: true, message: '', trigger: 'blur'}
      }
    }
  },
  methods: {
    handleSubmit() {
      axios.post(`api/user/${this.$store.state.userid}/change-passwd/`, this.form).then(resp => {
        this.modal = false
        this.form = {
          password1: '',
          password2: ''
        }
        this.$Message.success('Пароль был успешно изменен, пожалуйста, войдите в систему еще раз')
        this.$store.dispatch('logout').then(resp => {
          this.$router.push({name: 'login'})
        })
      }).catch(error => {
        this.$Notice.error({
          title: 'Сброс не удался',
          desc: JSON.stringify(error.response.data.msg)
        })
      })
    },
  }
}
</script>

<style scoped>
.container {
  padding-top: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
