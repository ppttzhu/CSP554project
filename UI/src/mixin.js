// global methods
export default {
  methods: {
    async search_mixin(index, query_json) {
      await this.$axios
        .post(index + "/_search", query_json, {
          headers: {
            "Content-Type": "application/json"
          }
        })
        .then(response => {
          console.log(response.data, "success");
          this.responseData = response.data;
        })
        .catch(error => (this.responseMessage = error));
    }
  }
};
