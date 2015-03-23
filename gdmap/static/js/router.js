// Filename: router.js
define([
  "jquery",
  "underscore",
  "backbone",
  "views/IndexView",
  "views/SearchView",
  "views/SongsView",
  "views/RecordingView",
  "views/RecordingsView"
], function($, _, Backbone, IndexView, SearchView, SongsView, RecordingView, RecordingsView){
  "use strict";
  var AppRouter = Backbone.Router.extend({
    routes: {
      "": "index",

      "search/": "searchSongs",
      "search/?:query": "searchSongs",

      "songs/": "songs",
      "songs/?:query": "songs",

      "recording/:show_id": "recording",

      "recordings/": "recordings",
      "recordings/?:query": "recordings",

      // Default
      "*actions": "defaultAction"
    },
    index: function() {
      var indexView = new IndexView();
      indexView.render(); 
    },
    searchSongs: function(query) {
      var params = this.parse_query_parameters(query);
      var searchView = new SearchView({"urlParams": params, "query": query, "router": this});
      searchView.render();
    },
    songs: function(query) {
      var params = this.parse_query_parameters(query);
      var songsView = new SongsView({"urlParams": params, "query": query});
      songsView.render();
    },
    recording: function(show_id) {
      var recordingView = new RecordingView({"show_id": show_id});
      recordingView.render();
    },
    recordings: function(query) {
      var params = this.parse_query_parameters(query);
      var recordingsView = new RecordingsView({"urlParams": params, "query": query});
      recordingsView.render();
    },
    defaultAction: function(actions) {
      console.log("No route:", actions);
    },
    parse_query_parameters: function(queryString) {
      // http://stackoverflow.com/questions/11671400/navigate-route-with-querystring
      var params = {};
        if(queryString){
          _.each(
            _.map(decodeURI(queryString).split(/&/g),function(el,i){
              var aux = el.split('='), o = {};
              if(aux.length >= 1){
                var val = undefined;
                if(aux.length == 2)
                  val = aux[1];
                o[aux[0]] = val;
              }
              return o;
            }),
            function(o){
              _.extend(params,o);
            }
          );
        }
      return params;
    }
  });

  var initialize = function(){
    var app_router = new AppRouter();
    // Navigate using urls rather than hashes
    // e.g. /songs/ rather than /#songs
    Backbone.history.start({pushState: true});
    // Use router.navigate for all urls
    // http://stackoverflow.com/questions/9328513/backbone-js-and-pushstate
    $(document).on('click', 'a:not([data-bypass])', function (evt) {

      var href = $(this).attr('href');
      var protocol = this.protocol + '//';

      if (href.slice(protocol.length) !== protocol) {
        evt.preventDefault();
        app_router.navigate(href, true);
      }
    });
  };
  return {
    initialize: initialize
  };
});