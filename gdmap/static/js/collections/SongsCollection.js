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
            // Track the number of other song recordings that matched this query
            var total = show.total;
            $.each(showSongs, function(index, song) {
                song.num_related = total - 1;
            });
            songs = songs.concat(showSongs);
        });
        return songs;
    }
  });
});