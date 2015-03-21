define([
  'backbone',
], function(Backbone){
  "use strict";
  return Backbone.Collection.extend({
    initialize: function(models, options) {
        this.models = models;
        this.options = options;
        this.url = "/api/songs/" + this.options.query;
    },
    parse: function(response) {
        return response.songs;
    }
  });
});