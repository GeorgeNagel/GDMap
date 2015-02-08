// Filename: router.js
define([
  "jquery",
  "underscore",
  "backbone",
  "views/IndexView",
  "views/SongsView"
], function($, _, Backbone, IndexView, SongsView){
  var AppRouter = Backbone.Router.extend({
    routes: {
      "": "index",
      "songs/": "songsList",

      // Default
      "*actions": "defaultAction"
    },
    index: function() {
      var indexView = new IndexView();
      indexView.render(); 
    },
    songsList: function() {
      var songsView = new SongsView();
      songsView.render();
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