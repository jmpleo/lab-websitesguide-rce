<template>
  <Modal
    v-model="modal3"
    title="Редактирование названия группы"
    footer-hide>
    <Form ref="form3" :model="form3" :label-width="120">
      <FormItem label="Название группы" prop="name" :rules="{required:true,message:'Название группы не может быть пустым',trigger:'blur'}"
                @keydown.native.enter.prevent="()=>{}">
        <Input ref="InputGroup" type="text" v-model="form3.name" clearable placeholder="Введите название группы"
               style="width: 300px;"></Input>
      </FormItem>
      <FormItem>
        <Row>
          <Col span="4" offset="14">
            <Button type="primary" @click="handleSubmit('form3')">Сохранить</Button>
          </Col>
          <Col span="4">
            <Button type="error" @click="handleCancel('form3')" style="margin-left: 8px">Отмена</Button>
          </Col>
        </Row>
      </FormItem>
    </Form>
  </Modal>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "editgroup",
        data() {
            return {
                modal3: false,
                id:'',
                form3: {
                    name:''
                },
            }
        },
        methods: {
            handleSubmit(name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        axios.put(`api/group/${this.id}/`,this.form3).then(resp=>{
                            this.$Message.success('Успешно сохранено');
                            this.handleCancel(name)
                            this.$parent.init()
                        }).catch(error=>{
                            this.$Message.err('Ошибка сохранения: '+error)
                            console.log(error)
                        })

                    }
                })
            },
            handleCancel(name) {
                this.modal3 = false
                this.$refs[name].resetFields()
            },
            inputFocus() {
                this.$nextTick(() => {
                    this.$refs['InputGroup'].focus()
                })
            }
        }
    }
</script>

<style scoped>

</style>
