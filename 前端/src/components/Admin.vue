<template>
    <div id="myBack">
        <div id="Select">
          
            <el-form :inline="true" :model="formInline" class="demo-form-inline">
            <el-form-item label="选择数据源">
                <el-select v-model="formInline.region" placeholder="选择数据源">
                <el-option label="中国疫情详细数据" value="china_details"></el-option>
                <el-option label="中国疫情历史数据" value="china_history"></el-option>
                <el-option label="中国疫情头版新闻" value="china_news"></el-option>
                <el-option label="全球城市疫情数据" value="city_details"></el-option>
                <el-option label="全球各国疫情数据" value="country_details"></el-option>
                <el-option label="全球历史疫情数据" value="global_history"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">查询</el-button>
                <el-button type="primary" @click="add">增加</el-button>
                <el-button type="danger" @click="mystatus">注销</el-button>
            </el-form-item>
            </el-form>
        </div>
        <div id="Show">
            <el-table height="100%" ref="goodsDetailTable" style="width: 100%" border :data="tableData" :default-sort = "{prop: 'date', order: 'descending'}">
            <template v-for="(item,index) in tableHead">
              <el-table-column :prop="item.column_name" :label="item.column_comment" sortable :key="index" v-if="item.column_name != 'id'" align="center" ></el-table-column>
            </template>
 
                <el-table-column label="操作" fixed="right" align="center" width="150">
            <template slot-scope="scope">
                  <el-button type="primary" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                  <el-button type="danger" size="small" @click="remove(scope.$index, scope.row)">删除</el-button>
            </template>
    </el-table-column>

          </el-table>
            
    <el-dialog :title="dialogTitle" width="50%" :visible.sync="iconFormVisible">
      <el-form :inline="true" :model="userInfo" class="demo-form-inline">
        <template v-for="(item,index) in tableHead">
        <el-form-item :label="item.column_comment" :key="index">
          <el-input v-model="userInfo[item.column_name]" :placeholder="item.column_comment"></el-input>
        </el-form-item>
        </template>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="iconFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitUser()">确 定</el-button>
      </div>
    </el-dialog>
        

        </div>

    </div>
</template>

<script>
  let flag=2;
  import qs from 'qs'
  import axios from 'axios'; 


 

  export default {
    data() {
      return {
        formInline: {
          region: ''
        },
        tableHead: [],
        tableData: [],
        dialogTitle: '编辑',
        iconFormVisible: false,
        userInfo: {},
        rowIndex: null
      }
    },
    methods: {

      mystatus() {
        const url = 'http://127.0.0.1:5000/pass'
        axios.post(url, {
              userName: 'admin',
              password: 'admin',   
              status: 0                 
              }).then((res) => {
                  if(res.data.code == 'success'){
                      console.log("to Global")
                      this.$router.replace("/");
                }                
              }).catch((error) => {

                        console.error(error);})
      },
                  getStatus() {
        const url = 'http://127.0.0.1:5000/getstatus';
        axios.get(url).then((res) => {
          this.logiinstatus = res.data.status
          if(this.logiinstatus == 0){
              this.$router.replace("/Load");
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },  

    // 增加
    add() {
      this.dialogTitle = '增加';
      this.iconFormVisible = true;
      this.userInfo = {};
    },
    // 编辑
    handleEdit(index, row) {
      this.dialogTitle = '编辑';
      this.userInfo = row;
      this.iconFormVisible = true;
      this.rowIndex = index;
    },
        // 弹窗确定
    submitUser() {
      if (this.dialogTitle === '编辑') {
        const url = 'http://127.0.0.1:5000/editData'
        var params = qs.stringify(this.userInfo)
        axios.post(url,{data: params,num: flag,type:'edit'}).then((res) => {
          console.log(res)
        }).catch((error) => {
          console.log(error)
        })
        this.tableData.splice(this.rowIndex, 1, this.userInfo);
        this.iconFormVisible = false;
        return;
      }
      else if (this.dialogTitle === '增加') {
        const url = 'http://127.0.0.1:5000/addData'
        var params = qs.stringify(this.userInfo)
        axios.post(url,{data: params,num: flag,type:'add'}).then((res) => {
          console.log(res)
        }).catch((error) => {
          console.log(error)
        })
      }
      this.tableData.splice(0, 0, this.userInfo);
      this.iconFormVisible = false;
    },
        // 删除
    remove(index, row) {
      // this.$confirm(`确定删除${row.column_comment}吗?`, '提示', {
      this.$confirm(`确定删除这条数据吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error',
      }).then(() => {
        this.tableData.splice(index, 1);
      });
      const url = 'http://127.0.0.1:5000/deleteData'
        var params = qs.stringify(row)
        axios.post(url,{data: params,num: flag,type:'delete'}).then((res) => {
          console.log(res)
        }).catch((error) => {
          console.log(error)
        })
    },
      onSubmit() {
        if (this.formInline.region=='china_details'){
            this.getdata(0)
            flag = 0
        }
        else if (this.formInline.region=='china_history'){
            this.getdata(1)

            flag = 1
        }
        else if (this.formInline.region=='china_news'){
            this.getdata(2)

            flag = 2
        }
        else if (this.formInline.region=='city_details'){
            this.getdata(3)

            flag = 3
        }
        else if (this.formInline.region=='country_details'){
            this.getdata(4)

            flag = 4
        }
        else if (this.formInline.region=='global_history'){
            this.getdata(5)

            flag = 5
        }
      },
      getdata(flag) {
        const url = 'http://127.0.0.1:5000/datalist'
        axios.post(url,{num: flag}).then((res) => {
          this.tableHead = res.data.datalist.tableHead
          this.tableData = res.data.datalist.tableData
                this.$nextTick(() => {
        this.$refs.goodsDetailTable.doLayout()
      })
        }).catch((error) => {
          console.log(error)
        })
      }
    },
    created() {
      this.getdata(flag);
      this.getStatus();
    },    
  }
</script>



<style scoped>
@import '../assets/css/Admin.css';
</style>