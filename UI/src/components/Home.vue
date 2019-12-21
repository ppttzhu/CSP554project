<template>
  <div id="app">
    <b-navbar toggleable="lg" type="light" variant="light" sticky="true">
      <b-navbar-brand href="#">诗词搜索</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item
            v-for="range in ranges"
            :key="range.englishName"
            :active="activeRange === range.englishName"
            @click="setRange(range.englishName)"
          >{{range.chineseName}}</b-nav-item>
          <b-nav-form>
            <b-form-input
              size="sm"
              class="mr-sm-2"
              @change="onSearch"
              @keydown.enter.prevent="routeSearch"
              v-model="query"
            ></b-form-input>
            <b-button size="sm" class="my-2 my-sm-0" type="submit" @click="routeSearch">搜索</b-button>
          </b-nav-form>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <div class="container" @scroll="onScroll">
      <div style="padding: 10px 0px 10px 0px">共找到 {{hit === 10000 ? "10000+" : hit}} 条结果：</div>
      <ul>
        <li v-for="content in contents" :key="content._id">
          <span
            v-if="content._source.title"
            v-html="content._source.title"
            style="padding-right:10px"
          ></span>
          <span v-else v-html="content._source.rhythmic" style="padding-right:10px"></span>
          <span v-html="content._source.author" style="padding-right:10px"></span>
          <div v-html="content._source.paragraphs"></div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import mixin from "../mixin.js";
export default {
  name: "Home",
  mixins: [mixin],
  data() {
    return {
      query: new URL(window.location.href).searchParams.get("query"),
      activeRange: new URL(window.location.href).searchParams.get("range")
        ? new URL(window.location.href).searchParams.get("range")
        : "all",
      responseData: null,
      responseMessage: null,
      hit: null,
      contents: null,
      ranges: [
        { englishName: "all", chineseName: "综合" },
        { englishName: "paragraphs", chineseName: "诗句" },
        { englishName: "title", chineseName: "标题" },
        { englishName: "author", chineseName: "作者" },
        { englishName: "start", chineseName: "句首" },
        { englishName: "end", chineseName: "句尾" }
      ]
    };
  },
  mounted() {
    this.submitSearch();
  },
  methods: {
    onScroll({ target: { scrollTop, clientHeight, scrollHeight } }) {
      if (scrollTop + clientHeight >= scrollHeight) {
        this.loadMore();
      }
    },
    loadMore() {
      console.log("load more");
    },
    routeSearch() {
      if (
        this.query !== null &&
        this.query !== undefined &&
        this.query !== ""
      ) {
        console.log("routeSearch");
        var searchParams = new URLSearchParams(window.location.search);
        searchParams.set("range", this.activeRange);
        searchParams.set("query", this.query);
        window.location.search = searchParams.toString();
      }
    },
    async submitSearch() {
      console.log("submitSearch");
      if (this.query) {
        await this.onSearch();
        this.processResponse();
      }
    },
    async onSearch() {
      console.log("onSearch");
      var query_json = this.prepareQuery();
      await this.search_mixin("poetry", query_json);
    },
    setRange(range) {
      this.activeRange = range;
    },
    prepareQuery() {
      var query_json = null;
      if (this.activeRange === "all") {
        var subquery_a = this.query.split(" ");
        var fields = ["paragraphs", "title", "rhythmic", "author"];
        var match_phrase_a = [];
        subquery_a.forEach(q => {
          var match_phrase_s = [];
          fields.forEach(f => {
            var match_phrase_f = {};
            match_phrase_f["match_phrase"] = {};
            match_phrase_f["match_phrase"][f] = q;
            match_phrase_s.push(match_phrase_f);
          });
          match_phrase_a.push({
            bool: {
              should: match_phrase_s
            }
          });
        });
        query_json = {
          query: {
            bool: {
              must: match_phrase_a
            }
          },
          highlight: {
            fields: [
              { paragraphs: {} },
              { title: {} },
              { rhythmic: {} },
              { author: {} }
            ]
          }
        };
      } else if (this.activeRange === "paragraphs") {
        var subquery_p = this.query.split(" ");
        var match_phrase_p = [];
        subquery_p.forEach(element => {
          match_phrase_p.push({ match_phrase: { paragraphs: element } });
        });
        query_json = {
          query: {
            bool: {
              must: match_phrase_p
            }
          },
          highlight: {
            fields: {
              paragraphs: {}
            }
          }
        };
      } else if (this.activeRange === "title") {
        query_json = {
          query: {
            bool: {
              should: [
                {
                  match_phrase: {
                    title: this.query
                  }
                },
                {
                  match_phrase: {
                    rhythmic: this.query
                  }
                }
              ]
            }
          },
          highlight: {
            fields: [{ title: {} }, { rhythmic: {} }]
          }
        };
      } else if (this.activeRange === "author") {
        query_json = {
          query: {
            match_phrase: {
              author: this.query
            }
          },
          highlight: {
            fields: {
              author: {}
            }
          }
        };
      } else if (this.activeRange === "start") {
        query_json = {
          query: {
            match_phrase: {
              paragraphs: "start" + this.query
            }
          },
          highlight: {
            fields: {
              paragraphs: {}
            }
          }
        };
      } else if (this.activeRange === "end") {
        query_json = {
          query: {
            match_phrase: {
              paragraphs: this.query + "end"
            }
          },
          highlight: {
            fields: {
              paragraphs: {}
            }
          }
        };
      }
      console.log(query_json);
      return query_json;
    },
    processResponse() {
      this.hit = this.responseData["hits"]["total"]["value"];
      this.contents = this.responseData["hits"]["hits"];
      this.contents.forEach(content => {
        // Apply Highlight
        if ("_source" in content && "highlight" in content) {
          for (var key in content["highlight"]) {
            content["highlight"][key].forEach(highlight_hit => {
              var highlight_hit_remove = highlight_hit
                .replace(new RegExp("<em>", "g"), "")
                .replace(new RegExp("</em>", "g"), "");
              if (Array.isArray(content["_source"][key])) {
                for (var i = 0; i < content["_source"][key].length; i++) {
                  content["_source"][key][i] = content["_source"][key][
                    i
                  ].replace(
                    new RegExp(highlight_hit_remove, "g"),
                    highlight_hit
                  );
                }
              } else {
                content["_source"][key] = content["_source"][key].replace(
                  new RegExp(highlight_hit_remove, "g"),
                  highlight_hit
                );
              }
            });
          }
        }
        // remove start & end
        if ("_source" in content && "paragraphs" in content._source) {
          content._source.paragraphs = content._source.paragraphs
            .join("")
            .replace(/start/g, "")
            .replace(/end/g, "");
        }
      });
    }
  }
};
</script>

<style>
em {
  color: #f1403c;
  font-style: normal;
  font-size: inherit;
}
</style>
