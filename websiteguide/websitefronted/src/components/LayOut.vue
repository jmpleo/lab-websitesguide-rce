<style scoped>
  .layout {
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
  }

  .layout-header-bar {
    background: #fff;
    box-shadow: 0 2px 3px 2px rgba(0, 0, 0, .1);
  }

</style>
<template>
  <div :style="{border:'none'}" class="layout">
    <SiderMenu></SiderMenu>
    <Layout :style="{marginLeft: '200px'}">
      <Header class="layout-header-bar">
        <div>
          <Row type="flex" justify="end" align="middle">
            <Dropdown transfer  @on-click="DropdownSelect" v-show="isShow">
              <!--                <Avatar :src="avatar" style="background: #2d8cf0; margin-left: 10px; "></Avatar>-->
              <div style="cursor: pointer;">
                <span v-text="username"></span>
                <Icon type="ios-arrow-down"></Icon>
              </div>
              <DropdownMenu slot="list">
                <DropdownItem name="center">Персональный центр</DropdownItem>
                <DropdownItem name="logout" divided>Выход из системы</DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </Row>
        </div>
      </Header>
      <Content :style="{padding: '0 16px 16px',}">
        <router-view v-wechat-title="$route.meta.title"></router-view>
      </Content>
    </Layout>
  </div>
</template>
<script>
    import SiderMenu from './SiderMenu'
    import Websites from './Websites'

    export default {
        name: 'LayOut',
        components: {
            Websites,
            SiderMenu
        },
        computed: {
            username() {
                return this.$store.state.username
            },
            isShow(){
              if (this.$route.meta.title !== "websiteguide"){
                return true
              }
        }},
        methods: {
            DropdownSelect(name) {
                if (name === 'logout') {
                    this.$store.dispatch('logout').then(resp => {
                        this.$router.push({name: 'login'})
                    })
                } else {
                    this.$router.push({name: 'center'})
                }
            }
        }
    }
</script>
