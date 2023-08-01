<template> <div class="container">
    <Content :style="{padding: '0 30px'}">
      <Card dis-hover>
        <div :style="{padding:'10px 0'}">
          <Row>
            <Col span="8">
              <div style="margin-bottom: 16px">
                <Button type="primary" size="default" icon="md-add" style="margin-right: 5px" @click="addUser">Добавить
                </Button>
              </div>
            </Col>
            <Col span="6" offset="10">
              <Input v-model="searchValue" search enter-button placeholder="поиск..."
                     @on-search="search"/>
            </Col>
          </Row>
          <Table :loading="loading" :columns="columns" :data="data">
            <template slot-scope="{ row }" slot="action" >
              <Button v-show="isSuperuser" type="warning" @click="forbidden(row)">
                <span v-if="isActive(row)">Запретить</span>
                <span v-else>Разрешить</span>
              </Button>
              <Button v-show="isSuperuser" type="primary" @click="resetPassword(row)">Сбросить пароль
              </Button>
              <Button v-show="isSuperuser" type="info" @click="editUser(row)">Редактировать</Button>
              <Button v-show="isSuperuser" type="error" @click="remove(row)">Удалить</Button>
            </template>
          </Table>
          <br>
          <Page :total="total" :page-size="size" show-sizer show-total style="text-align: center"
                @on-change="pageNum" @on-page-size-change="pageSize"></Page>
        </div>
      </Card>
    </Content>
    <adduserform ref="adduserform"></adduserform>
    <resetpassword ref="resetpassword"></resetpassword>
    <edituserform ref="edituserform"></edituserform>
  </div>
</template>

<script>
    import init from "../../../mixins/init";
    import adduserform from "./module/adduserform";
    import resetpassword from "./module/resetpassword";
    import edituserform from "./module/edituserform";
    import axios from 'axios'

    export default {
        components: {adduserform, resetpassword, edituserform},
        data() {
            return {
                searchValue: '',
                columns: [
                    {
                        type: 'index',
                        title: '№',
                        width: '90',
                    },
                    {
                        title: 'Имя пользователя',
                        key: 'username'
                    },
                    {
                        title: 'Имя',
                        key: 'alias',
                    },
                    {
                        title: 'Статус',
                        render: (h, params) => {
                            if (this.data[params.index].is_active) {
                                return h("Badge", {props: {status: "success", text: "Активен"}},)
                            } else {
                                return h("Badge", {props: {status: "default", text: "Запрещен"}},)
                            }
                        },
                        width: '200'
                    },
                    {
                        title: 'Действия',
                        slot: 'action',
                        width: '350'
                    }
                ],
            }
        },
        mixins: [init],
        created() {
            this.$nextTick(() => {
                this.init()
            })
        },
        computed:{
          isSuperuser(){
            return this.$store.state.is_superuser
          }
        },
        methods: {
            beforeInit() {
                this.url = 'api/user/'
                this.params = {page: this.page, size: this.size}
                return true
            },
            isActive(row) {
                console.log("hellow",row)
                return row.is_active
            },
            addUser() {
                this.$refs['adduserform'].modal = true
                //инициализация данных, чтобы избежать автоматического заполнения имени пользователя и пароля
                this.$refs['adduserform'].form = {
                    username: '',
                    alias: '',
                    password: ''
                }
            },
            forbidden(row) {
                this.$Modal.confirm({
                    title: "Подтверждение действия",
                    content: `<p>Вы уверены, что хотите ${row.is_active ? 'запретить' : 'разрешить'} ${row.username} ? </p>`,
                    onOk: () => {
                        axios.patch(`api/user/${row.id}/`, {"is_active": !row.is_active}).then(resp => {
                            this.$Message.success('Действие выполнено успешно')
                            this.init()
                        }).catch(error => {
                            this.init()
                            this.$Message.error('Ошибка выполнения действия')
                        })
                    },
                    onCancel: () => {
                    }
                })

            },
            search(val) {
                if (val) {
                    axios.get(`api/user/?page=1&size=${this.size}&search=${this.searchValue}`).then(resp => {
                        this.total = resp.data.count
                        this.data = resp.data.results
                    })
                } else {
                    this.page = 1
                    this.init()
                }
            },
            resetPassword(row) {
                this.$refs['resetpassword'].modal = true
                this.$refs['resetpassword'].rowId = row.id
            },
            editUser(row) {
                console.log(row)
                this.$refs['edituserform'].modal = true
                this.$refs['edituserform'].rowId = row.id
                this.$refs['edituserform'].form = {
                    username: row.username,
                    alias: row.alias,
                }
            },
            remove(row) {
                this.$Modal.confirm({
                    title: "Подтверждение удаления",
                    content: `<p>Вы уверены, что хотите удалить ${row.username} ? </p>`,
                    onOk: () => {
                        axios.delete(`api/user/${row.id}`).then(resp => {
                            this.$Message.success('Удаление выполнено успешно')
                            this.init()
                        }).catch(error => {
                            this.$Notice.error({
                                title: 'Ошибка удаления',
                                desc: JSON.stringify(error.response.data)
                            })
                        })
                    },
                    onCancel: () => {
                    }
                })

            }
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
