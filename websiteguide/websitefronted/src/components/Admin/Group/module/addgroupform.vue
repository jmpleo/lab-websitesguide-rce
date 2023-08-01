<template>
  <Modal
    v-model="modal1"
    title="Добавление группы"
    footer-hide>
    <Form ref="form1" :model="form1" :label-width="120">
      <FormItem label="Название группы"  prop="name" :rules="{required:true,message:'Название группы не может быть пустым',trigger:'blur'}" @keydown.native.enter.prevent ="()=>{}">
        <Input ref="InputGroup" type="text"  v-model="form1.name" clearable  placeholder="Введите название группы" style="width: 300px;" ></Input>
      </FormItem>
      <FormItem>
        <Row>
          <Col span="4" offset="14">
            <Button type="primary" @click="handleSubmit('form1')">Добавить</Button>
          </Col>
          <Col span="4">
            <Button type="error" @click="handleCancel('form1')" style="margin-left: 12px">Отмена</Button>
          </Col>
        </Row>
      </FormItem>
    </Form>
  </Modal>
</template>

<script>
    import axios from 'axios'
    export default {
        name: "addgroupform",
        data() {
            return {
                modal1: false,
                form1: {
                    name: ''
                },
            }
        },
        methods: {
            handleSubmit(name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        axios.post('api/group/',this.form1).then(resp=>{
                            this.$Message.success('Группа успешно добавлена');
                            this.handleCancel(name)
                            console.log(this.$parent)
                            this.$parent.init()
                        }).catch(error=>{
                            this.$Message.err('Ошибка добавления: '+error)
                            console.log(error)
                        })
                    }
                })
            },
            handleCancel(name) {
                this.modal1 = false
                this.$refs[name].resetFields()
                this.form1={name: ''}
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
