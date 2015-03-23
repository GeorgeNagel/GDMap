define([
  'underscore',
  'backbone',
  'mustache',
  'text!templates/song.mustache'
], function(_, Backbone, Mustache, songtemplate){
  "use strict";
  return Backbone.View.extend({
    initialize: function(model, options) {
        this.model = model;
        this.options = options;
    },
    render: function(){
      var modelJSON = _.clone(this.model.attributes);


      if (this.options) {
        // Add the songs url to the JSON blob
        var query_parameters = this.options.query_parameters;
        modelJSON.songs_url = this.build_songs_url(query_parameters);
      }

      var rendered = Mustache.render(songtemplate, modelJSON);
      return rendered;
    },
    build_songs_url: function(query_parameters) {
      // Return a url for the /songs/ view
      var url = '/songs/?album=' + this.model.attributes.album;

      if (query_parameters) {
        // Keep track of relevant parameters for a songs page
        // For example, we don't want to keep pagination
        var songs_query_parameters = {};

        if (query_parameters.q) {
          songs_query_parameters.q = query_parameters.q;
        }
        if (query_parameters.sort) {
          songs_query_parameters.sort = query_parameters.sort;
        }
        if (query_parameters.sort_order) {
          songs_query_parameters.sort_order = query_parameters.sort_order;
        }

        $.each( songs_query_parameters, function(key, value) {
          url = url + "&"+ key + "=" + value;
        });
      }
      return url;
    }
  })
})