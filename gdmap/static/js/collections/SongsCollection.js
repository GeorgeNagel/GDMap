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
        return response.songs;
    }
  });
});