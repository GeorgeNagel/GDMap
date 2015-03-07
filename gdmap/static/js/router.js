// Filename: router.js
define([
  "jquery",
  "underscore",
  "backbone",
  "views/IndexView",
  "views/SearchView",
  "views/SongsView",
  "views/RecordingView",
], function($, _, Backbone, IndexView, SearchView, SongsView, RecordingView){
  "use strict";
  var AppRouter = Backbone.Router.extend({
    routes: {
      "": "index",
      "search/": "searchSongs",
      "search/?:query": "searchSongs",
      "songs/": "songs",
      "songs/?:query": "songs",
      "recording/:show_id": "recording",

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
    songs: function(query) {
      var songsView = new SongsView({"query": query});
      songsView.render();
    },
    recording: function(show_id) {
      var recordingView = new RecordingView({"show_id": show_id});
      recordingView.render();
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