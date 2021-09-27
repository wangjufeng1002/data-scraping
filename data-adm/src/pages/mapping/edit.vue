<template>
  <div>
    <el-form
      label-position="left"
      label-width="80px"
      :model="childEditForm"
    >
      <el-form-item label="当当Id">
        <el-input v-model="childEditForm.productId" :disabled="this.edit"></el-input>
      </el-form-item>
      <el-form-item label="外站Id">
        <el-input v-model="childEditForm.outerCode"></el-input>
      </el-form-item>
      <el-form-item label="外站SKU">
        <el-input v-model="childEditForm.outerSku"></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="onCancel">取 消</el-button>
      <el-button type="primary" @click="onsubmit">确 定</el-button>
    </span>
  </div>
</template>
<script>
import {submitMapping} from './request'
export default {
  props: {
    edit:Boolean,
    editForm:Object,
    onCancel: Function,
  },
  data(){
      return{
          childEditForm:this.editForm
      }
  },
  methods:{
      //确认提交
      async onsubmit(){
        const params={
          id:this.childEditForm.id,
          ddProductId:this.childEditForm.productId,
          outerProductId:this.childEditForm.outerCode
        }
        const {data}=  await submitMapping(params)
        if(data.code===0){
          this.$message({message:'绑定成功', type: 'success'});
          this.onCancel()
        }else{
          this.$message.error('绑定失败');
        }
    
      }

  },
  beforeUpdate(){
        this.childEditForm=this.editForm
  },
  setup() {
  },
};
</script>