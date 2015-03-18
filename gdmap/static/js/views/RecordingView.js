define([
  'backbone',
  'mustache',
  'collections/RecordingsCollection',
  'text!templates/recording.mustache',
  'views/MapView',
  'utils',
], function(Backbone, Mustache, RecordingsCollection, recordingtemplate, MapView, utils){
  "use strict";
  return Backbone.View.extend({
    el: $("#container"),
    initialize: function(options) {
      var self = this;
      var showID = options.show_id;
      var query = "show_id=" + showID;
      // Query for the single recording
      var recordings = new RecordingsCollection([], {query: query})
      recordings.fetch({
        success: function() {
          self.render();
        }
      });
      this.recordings = recordings;
    },
    render: function(){
      this.$el.html("<h1>Recording</h1>");
      var recording = this.recordings.first();
      if (recording) {
        // Render the map
        var latlons = utils.modelsLatLons([recording]);
        var mapview = new MapView(null, {latlons: latlons});
        mapview.render();
        // Render the recording
        var rendered = Mustache.render(recordingtemplate, recording.attributes);
        this.$el.append(rendered);
      }
    }
  })
})