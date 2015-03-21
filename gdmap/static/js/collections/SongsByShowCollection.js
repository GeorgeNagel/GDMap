define([
  'collections/BaseCollection'
], function(BaseCollection){
  "use strict";
  return BaseCollection.extend({
    initialize: function(models, options) {
      this.models = models;
      this.options = options;
      var query = options.query || "";
      this.options.query_parameters = this.parse_query_parameters(query);
      this.baseUrl = "/api/songs-by-show/";
      this.url = this.baseUrl + "?" + query;
    },
    updateParameters: function(new_query_parameters) {
      for (var key in new_query_parameters) {
        this.options.query_parameters[key] = new_query_parameters[key];
      }
      var query = this.buildQuery(this.options.query_parameters);
      this.url = this.baseUrl + "?" + query;
    },
    buildQuery: function(query_parameters) {
      var newQueryParameters = [];
      for (var key in query_parameters) {
        newQueryParameters.push(key + "=" + query_parameters[key]);
      }
      var newQuery = newQueryParameters.join("&");
      return newQuery;
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