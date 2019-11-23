<template>
  <div id="app" class="container">
    <div class="input-group input-group-lg bottom">
      <div class="input-group-prepend">
        <span class="input-group-text">Search</span>
      </div>
      <input type="text" class="form-control col-md-6" @keyup.prevent="search" v-model="query" />
    </div>
    <div>{{data}}</div>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      query: "",
      data: []
    };
  },
  methods: {
    search() {
      var query_json = {
        query: {
          match: {
            author: {
              query: this.query,
              operator: "and"
            }
          }
        }
      };
      this.axios
        .post("http://localhost:9200/testpoetry/_search?pretty", query_json, {
          headers: {
            "Content-Type": "application/json"
          }
        })
        .then(response => {
          console.log(response.data);
          this.data = response.data;
        });
    }
  }
};
</script>

<style>
.bottom {
  margin-top: 50px;
  margin-left: 200px;
}
</style>
