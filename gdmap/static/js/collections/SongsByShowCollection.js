define([
  'backbone'
], function(BaseCollection){
  "use strict";
  return Backbone.Collection.extend({
    initialize: function(models, options) {
      this.models = models;
      this.options = options;
      this.url = "/api/songs-by-show/?" + this.options.query;
    },
    parse: function(response) {
      // Parse pagination information
      this.page = response.page;
      this.per_page = response.per_page;
      this.total = response.total;
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
    },
    hasNextPage: function() {
      if (this.total > this.page * this.per_page) {
        return true;
      } else {
        return false;
      }
    },
    hasPreviousPage: function() {
      if (this.page > 1) {
        return true;
      } else {
        return false;
      }
    }
  });
});