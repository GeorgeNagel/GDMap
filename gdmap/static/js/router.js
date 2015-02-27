// Filename: router.js
define([
  "jquery",
  "underscore",
  "backbone",
  "views/IndexView",
  "views/SearchView",
  "views/ShowView",
], function($, _, Backbone, IndexView, SearchView, ShowView){
  var AppRouter = Backbone.Router.extend({
    routes: {
      "": "index",
      "search/": "searchSongs",
      "search/?:query": "searchSongs",
      "show/:show_id": "show",

      // Default
      "*actions": "defaultAction"
    },
    index: function() {
      var indexView = new IndexView();
      indexView.render(); 
    },
    searchSongs: function(query) {
      var searchView = new SearchView({"query": query});
      searchView.render();
    },
    show: function(show_id) {
      var showView = new ShowView({"show_id": show_id});
      showView.render();
    },
    defaultAction: function(actions) {
        console.log("No route:", actions);
    }
  });

  var initialize = function(){
    var app_router = new AppRouter();
    // Navigate using urls rather than hashes
    // e.g. /songs/ rather than /#songs
    Backbone.history.start({pushState: true});
  };
  return {
    initialize: initialize
  };
});