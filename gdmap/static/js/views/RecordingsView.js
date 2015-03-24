define([
  'backbone',
  'collections/RecordingsCollection',
  'views/RecordingResultView',
  'views/MapView',
  'utils',
], function(Backbone, RecordingsCollection, RecordingResultView, MapView, utils){
  "use strict";
  return Backbone.View.extend({
    el: $("#content"),
    initialize: function(options) {
      var self = this;
      var recordings = new RecordingsCollection([], options);
      recordings.fetch({
        success: function() {
          self.render()
        }
      });
      this.recordings = recordings;
    },
    render: function(){
      var self = this;
      self.$el.html("<h1>Recordings</h1>");

      // Render the map
      var latlons = utils.modelsLatLons(self.recordings.models);
      var mapview = new MapView(null, {latlons: latlons});
      mapview.render();

      // Render the recordings list
      self.recordings.each(function(recording) {
        var view = new RecordingResultView(recording);
        self.$el.append(view.render());
      });
    }
  })
})