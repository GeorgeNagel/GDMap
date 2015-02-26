define([
  'backbone',
], function(Backbone){
  "use strict";
  return Backbone.Collection.extend({
    initialize: function(models, options) {
        this.models = models;
        this.options = options;
        var query = "?" + options.query || "";
        this.url = "/api/songs/" + query;
    },
    parse: function(response) {
        // Parse the songs out of the songs-by-show response
        var songs = []
        $.each(response.songs_by_show, function(index, show) {
            var showSongs = show.songs;
            songs = songs.concat(showSongs);
        });
        return songs;
    }
  });
});