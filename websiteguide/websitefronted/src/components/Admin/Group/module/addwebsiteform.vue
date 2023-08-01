<template>
  <Modal
    v-model="modal2"
    width="700"
    :title="rowData.rowName"
    :closable="false"
    :mask-closable="false"
    footer-hide
    id="modal2">
    <Form ref="form2" :model="form2" :label-width="80" style="width: 700px">
      <FormItem
        v-for="(item,index) in form2.items"
        :key="index"
        :label="''+(index+1)">
        <FormItem>
          <Row>
            <Col span="16">
              <FormItem label="URL" :prop="'items.'+index+'.path'" :rules="rules.path" style="display: flex">
                <Input type="text" v-model="item.path" clearable placeholder="Введите URL" style="width: 300px;"></Input>
              </FormItem>
            </Col>
            <Col span="4">
              <Button v-if="form2.items.length > 1" type="error" @click="handleRemove(index)">Удалить</Button>
            </Col>
          </Row>
        </FormItem>
        <FormItem>
          <Row>
            <Col span="16">
              <FormItem label="Заголовок" :prop="'items.'+index+'.title'" :rules="rules.title"
                        style="display: flex;margin-top: 20px">
                <Input type="text" v-model="item.title" clearable placeholder="Введите заголовок" clearable
                       style="width: 300px"></Input>
              </FormItem>
            </Col>
          </Row>
        </FormItem>
        <FormItem>
          <Row>
            <Col span="16">
              <FormItem label="Описание" :prop="'items.'+index+'.description'" :rules="rules.description"
                        style="display: flex;margin-top: 20px">
                <Input type="text" v-model="item.description" clearable placeholder="Введите описание" clearable
                       style="width: 300px;"></Input>
              </FormItem>
            </Col>
          </Row>
        </FormItem>
<!--        <FormItem>-->
<!--          <Row>-->
<!--            <Col span="16">-->
<!--              <FormItem label="Иконка" :prop="'items.'+index+'.description'" :rules="rules.description"-->
<!--                        style="display: flex;margin-top: 20px">-->
<!--                <Upload-->
<!--                  :before-upload="handleUpload"-->
<!--                  action="//jsonplaceholder.typicode.com/posts/">-->
<!--                  <Button icon="ios-cloud-upload-outline">Загрузить иконку</Button>-->
<!--                </Upload>-->
<!--                <div v-if="item.file !== null">Загруженный файл: {{ item.file.name }}-->
<!--                  <Button type="text" @click="upload" :loading="loadingStatus">-->
<!--                    {{ loadingStatus ? 'Загрузка' : 'Нажмите, чтобы загрузить' }}-->
<!--                  </Button>-->
<!--                </div>-->
<!--              </FormItem>-->
<!--            </Col>-->
<!--          </Row>-->
<!--        </FormItem>-->
      </FormItem>
      <FormItem>
        <Row>
          <Col span="8" offset="4">
            <Button type="dashed" long @click="handleAdd" icon="md-add">Добавить элемент</Button>
          </Col>
        </Row>
      </FormItem>
      <FormItem>
        <Row>
          <Col span="3" offset="16">
            <Button type="primary" @click="handleSubmit('form2')">Отправить</Button>
          </Col>
          <Col span="3">
            <Button type="error" @click="handleCancel('form2')" style="margin-left: 8px">Отмена</Button>
          </Col>
        </Row>


      </FormItem>
    </Form>
  </Modal>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'addwebsiteform',
        props: {
            rowData: {
                type: Object,
                required: true
            }
        },
        data() {
            return {
                modal2: false,
                loadingStatus: false,
                form2: {
                    items: [
                        {
                            path: '',
                            title: '',
                            description: '',
                            website_group: '',
                        }
                    ]
                },
                rules: {
                    path: {required: true, message: 'URL не может быть пустым', trigger: 'blur'},
                    title: {required: true, message: 'Заголовок не может быть пустым', trigger: 'blur'},
                    description: {}

                }
            }
        },
        methods: {
            // handleUpload(file) {
            //     console.log(file)
            //     this.file = file;
            //     return false;
            // },
            // upload() {
            //     this.loadingStatus = true;
            //     setTimeout(() => {
            //         this.file = null;
            //         this.loadingStatus = false;
            //         this.$Message.success('Успешно')
            //     }, 1500);
            // },
            handleSubmit(name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        this.form2.items.map(val => {
                            val.website_group = this.rowData.rowId
                        })
                        axios.post('api/website/', this.form2.items).then(resp => {
                            this.handleCancel(name),
                                this.$Message.success('Успешно добавлено')
                            this.$parent.init()
                        }).catch(error => {
                            this.$Modal.warning({
                                title: 'Ошибка',
                                content: JSON.stringify(error.response.data.detail)
                            })
                        })
                    } else {
                        this.$Message.error('Ошибка!');
                    }
                })
            },
            handleCancel(name) {
                this.modal2 = false
                this.$refs[name].resetFields()
                this.form2.items = [{path: '', title: '', description: '', website_group: ''}]

            },
            handleAdd() {
                this.form2.items.push({
                    path: '',
                    title: '',
                    description: '',
                    website_group: ''
                });
            },
            handleRemove(index) {
                this.form2.items.splice(index, 1)
            }
        }
    }
</script>

<style scoped>

</style>
