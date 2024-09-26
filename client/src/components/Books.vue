<template>
  <!-- main table -->
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-10">
        <h1>业财对账系统</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button
            type="button"
            class="btn btn-danger btn-sm between"
            @click="toggleSubmitConfirmModal">
            提交
          </button>
        <br><br>
        <table class="table">
          <thead>
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
              <td><input
                  type="number"
                  class="form-control"
                  id="addReason"
                  :disabled=book.check
                  v-model=book.modified_sum
                  placeholder="请输入核对金额"></td>
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
                    class="btn btn-success btn-sm between"
                    @click="handleCheck(book)"
                    v-if="book.check">
                    已对账
                  </button>
                  <button
                    type="button"
                    class="btn btn-warning btn-sm between"
                    @click="handleCheck(book)"
                    v-else>
                    对账
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
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <!-- <div class="modal-header"> -->
            <!-- <h4 class="modal-title">是否确认提交已对账订单？确认后将不能更改</h4> -->
            <!-- <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleSubmitConfirmModal">
              <span aria-hidden="true">&times;</span>
            </button> -->
          <!-- </div> -->
          <div class="modal-body">
            是否确认提交已对账订单？<br>
            确认后将不能更改！<br><br>
            <!-- <form> -->
              <!-- <div class="mb-3">
                <label for="addBookTitle" class="form-label">Title:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addBookTitle"
                  v-model="addBookForm.title"
                  placeholder="Enter title">
              </div>
              <div class="mb-3">
                <label for="addBookAuthor" class="form-label">Author:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addBookAuthor"
                  v-model="addBookForm.author"
                  placeholder="Enter author">
              </div>
              <div class="mb-3 form-check">
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="addBookRead"
                  v-model="addBookForm.read">
                <label class="form-check-label" for="addBookRead">Read?</label>
              </div> -->
              <!-- <div class="btn-group" role="group"> -->
                <button
                  type="button"
                  class="btn btn-danger btn-sm between"
                  @click="handleSubmit(books)">
                  确认
                </button>
                <button
                  type="button"
                  class="btn btn-primary btn-sm between"
                  @click="toggleSubmitConfirmModal">
                  取消
                </button>
              <!-- </div> -->
            <!-- </form> -->
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeSubmitConfirmModal" class="modal-backdrop fade show"></div>   
    <!-- edit book modal -->
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      activeSubmitConfirmModal: false,
      button:'对账',
      books: [],
      
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
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
          this.message = 'Orders Submited!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getBooks();
        });
    },
    toggleSubmitConfirmModal(){
      this.activeSubmitConfirmModal=!this.activeSubmitConfirmModal
    }
  },
    
  created() {
    this.getBooks();
  },
 
};

</script>

<style>
.between {
 margin-right: 8px;
}
</style>
