<template>
  <div class="me-allct-body" v-title :data-title="categoryTagTitle" >
    <el-container class="me-allct-container">
      <el-main>
        <el-tabs v-model="activeName">
          <el-tab-pane label="分类" name="category">
            <ul class="me-allct-items">
              <li v-for="c in categories" @click="view(c.id,c.article_counts)" :key="c.id" class="me-allct-item">
                <div class="me-allct-content">
                  <a class="me-allct-info">
                    <img class="me-allct-img" :src="c.avatar?c.avatar:defaultAvatar"/>
                    <h4 class="me-allct-name">{{c.categoryname}}</h4>
                    <p class="me-allct-description">{{c.description}}</p>
                  </a>

                  <div class="me-allct-meta">
                    <span>{{c.article_counts}} 文章</span>
                  </div>
                </div>
              </li>
            </ul>
          </el-tab-pane>
          <el-tab-pane label="标签" name="tag">
            <ul class="me-allct-items">
              <li v-for="t in tags" @click="view(t.id,t.article_counts)" :key="t.id" class="me-allct-item">
                <div class="me-allct-content">
                  <a class="me-allct-info">
                    <img class="me-allct-img" :src="t.avatar?t.avatar:defaultAvatar"/>
                    <h4 class="me-allct-name">{{t.tagname}}</h4>
                  </a>

                  <div class="me-allct-meta">
                    <span>{{t.article_counts}}  文章</span>
                  </div>
                </div>
              </li>
            </ul>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import defaultAvatar from '@/assets/img/logo.png'
  import {reqAllCategories} from '@/api/category'
  import {reqAllTags} from '@/api/tag'

  export default {
    name: 'BlogAllCategoryTag',
    created() {
      this.getCategorys()
      this.getTags()
    },
    data() {
      return {
        defaultAvatar:defaultAvatar,
        categories: [],
        tags: [],
        currentActiveName: 'category'
      }
    },
    computed: {
      activeName: {
        get() {
          if(!this.$route.params.type){
            return (this.currentActiveName = 'category')
          }
          return (this.currentActiveName = this.$route.params.type)
        },
        set(newValue) {
          this.currentActiveName = newValue
        }
      },
      categoryTagTitle (){
        if(this.currentActiveName === 'category' || this.currentActiveName === '0'){
          return '文章分类  - 别院牧志'
        }
        return '标签  - 别院牧志'
      }
    },
    methods: {
      view(id,itemCount) {
        if(itemCount > 0){
          this.$router.push({path: `/${this.currentActiveName}/${id}`})
        }else{
          this.$message.warning({
            message: '该技能树暂未点亮，请探索其他领域哦~',
            center: true,
            offset: 55
          });
        }
      },
      getCategorys() {
        let that = this
        reqAllCategories().then(data => {
          that.categories = data.data
        }).catch(error => {
          if (error !== 'error') {
            that.$message.error({message: '文章分类加载失败', showClose: true})
          }
        })
      },
      getTags() {
        let that = this
        reqAllTags().then(data => {
          that.tags = data.data
        }).catch(error => {
          if (error !== 'error') {
            that.$message.error({message: '标签加载失败', showClose: true})
          }
        })
      }
    },
    //组件内的守卫 调整body的背景色
    beforeRouteEnter(to, from, next) {
      window.document.body.style.backgroundColor = '#fff';
      next();
    },
    beforeRouteLeave(to, from, next) {
      window.document.body.style.backgroundColor = '#f5f5f5';
      next();
    }
  }
</script>

<style>
  .me-allct-body {
    margin: 60px auto 140px;
  }

  .me-allct-container {
    width: 1000px;
  }

  .me-allct-items {
    padding-top: 2rem;
  }

  .me-allct-item {
    width: 25%;
    display: inline-block;
    margin-bottom: 2.4rem;
    padding: 0 .7rem;
    box-sizing: border-box;
  }

  .me-allct-content {
    display: inline-block;
    width: 100%;
    background-color: #fff;
    border: 1px solid #f1f1f1;
    transition: border-color .3s;
    text-align: center;
    padding: 1.5rem 0;
  }

  .me-allct-info {
    cursor: pointer;
  }

  .me-allct-img {
    margin: -40px 0 10px;
    width: 60px;
    height: 60px;
    vertical-align: middle;

  }

  .me-allct-name {
    font-size: 21px;
    font-weight: 200;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-top: 4px;
  }

  .me-allct-description {
    min-height: 50px;
    font-size: 13px;
    line-height: 25px;
  }

  .me-allct-meta {
    font-size: 12px;
    color: #969696;
  }
</style>
