<template>
  <!-- main table -->
  <div class="container text-center">
    <div class="row">
      <div class="col-md-1">
        <h2>
        <alert :message="message" v-if="showMessage" @close-alert="handleCloseAlert" />
          <button
            type="button"
            class="btn btn-danger"
            @click="toggleSubmitConfirmModal">
            提交
          </button>
        </h2>
      </div>
    </div>  
    <div class="row">
      <div class="table-responsive">
          
        <table class="table align-middle">
          <thead class="table-head">
            <tr>
              <th scope="col">订单号</th>
              <th scope="col">下单时间</th>
              <th scope="col">结算时间</th>
              <th scope="col">订单金额</th>
              <th scope="col">账单金额</th>
              <th scope="col">差异</th>
              <th scope="col">核对金额</th>
              <th scope="col">差异原因</th>
              <th scope="col">对账处理</th>
            </tr>
          </thead>
    
          <tbody>
            <tr v-for="book in books" :key="book.order_id">
              <td>{{ book.sales_order }}</td>
              <td>{{ book.deal_time }}</td>
              <td>{{ book.settle_time }}</td>
              <td>{{ book.order_sum }}</td>
              <td>{{ book.bill_sum }}</td>
              <td>{{ book.variance }}</td>
              <td>
                <div>
                <input
                  type="tel"
                  class="form-control"
                  id="addReason"
                  :disabled=book.check
                  v-model=book.modified_sum
                  placeholder="请输入核对金额">
                </div>
                </td>
              <td>
                <input
                  type="text"
                  class="form-control"
                  id="addReason"
                  :disabled=book.check
                  v-model=book.reason
                  @blur="updateBookTitle(book.reason)"
                  placeholder="请输入差异原因">
              </td>
              <td>
                <div>
                  <button
                    type="button"
                    class="btn btn-success"
                    @click="handleCheck(book)"
                    v-if="book.check">
                    已对账
                  </button>
                  <button
                    type="button"
                    class="btn btn-warning"
                    @click="handleCheck(book)"
                    v-else>
                    未对账
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      
    </div>
    </div>

    <!-- submit confirm modal -->
    <div
      ref="addBookModal"
      class="modal fade"
      :class="{ show: activeSubmitConfirmModal, 'd-block': activeSubmitConfirmModal }"
      tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="toggleSubmitConfirmModal">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <p class="text-center">提交后“已对账”将不能更改，“未对账”将会暂存。<br>是否确认提交？</p>
          </div>
          <div class="modal-footer">
            <div class="d-flex justify-content-center">
                <button
                  type="button"
                  class="btn btn-primary between"
                  @click="handleSubmit(books)">
                  确认
                </button>
                <button
                  type="button"
                  class="btn btn-secondary between"
                  data-dismiss="modal"
                  @click="toggleSubmitConfirmModal">
                  取消
                </button>
              </div>
              </div>
              <!-- </div> -->
            <!-- </form> -->
          </div>
        </div>
      </div>
    <div v-if="activeSubmitConfirmModal" class="modal-backdrop fade show"></div>   
   </div> 
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';


export default {
  data() {
    return {
      activeSubmitConfirmModal: false,
      books: [],
      showMessage: false,
    };
  },
  components: {
    Alert,
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5001/books';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    updateSum(newSum){
      book.modified_sum=newSum;
    },
    updateReason(newReason) {
      book.reason = newReason;
    },
    handleCheck(book) {
      book.check=!book.check
    },
    handleSubmit(books){
      const path = `http://localhost:5001/books/submit`
      axios.post(path,books)
        .then(() => {
          this.toggleSubmitConfirmModal()
          this.getBooks()
          this.message = '“已对账”提交成功！“未对账”已暂存！';
          this.showMessage = true;

        })
        .catch((error) => {
          console.error(error);
          this.getBooks();
        });
    },
    toggleSubmitConfirmModal(){
      this.activeSubmitConfirmModal=!this.activeSubmitConfirmModal
    },
    handleCloseAlert() {
      this.showMessage = false;
    },
  },

  created() {
    this.getBooks();
  },
  mounted() {
    // 确保在文档加载完成后初始化tooltip
    this.$nextTick(function () {
      $('[data-toggle="tooltip"]').tooltip({
        trigger: 'hover' // 触发方式可以是hover或者click
      });
    });
  }
};

</script>

<style>
.table-responsive {
  position: relative;
  overflow-y: auto;
}
.table-head th {
  position: sticky;
  top: 0;
  z-index: 1;
  background-color: #fff; /* 背景颜色可以根据需要设置 */
}
</style>