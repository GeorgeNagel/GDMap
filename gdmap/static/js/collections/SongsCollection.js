define([
  'backbone',
], function(Backbone){
  "use strict";
  return Backbone.Collection.extend({
    url: "/api/songs/",
    parse: function(response) {
        var songs = response.songs;
        return songs;
    }
  });
});