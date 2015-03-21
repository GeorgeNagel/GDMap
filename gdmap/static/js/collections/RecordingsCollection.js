define([
  'backbone'
], function(BaseCollection){
  "use strict";
  return Backbone.Collection.extend({
    initialize: function(models, options) {
        this.models = models;
        this.options = options;
        this.url = "/api/recordings/" + "?" + this.options.query;
    },
    parse: function(response) {
        // Parse the recordings
        return response.recordings;
    }
  });
});