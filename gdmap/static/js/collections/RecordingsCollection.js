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
        this.url = "/api/recordings/" + "?" + query;
    },
    parse: function(response) {
        // Parse the recordings
        return response.recordings;
    }
  });
});