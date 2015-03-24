define([
  'backbone',
  'mustache',
  'collections/RecordingsCollection',
  'views/RecordingResultView',
  'views/MapView',
  'text!templates/listpage.mustache',
  'utils',
], function(Backbone, Mustache, RecordingsCollection, RecordingResultView, MapView, listpage, utils){
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
      // Render the basic template
      var pageRendered = Mustache.render(listpage);
      this.$el.html(pageRendered);

      $("#menu").html("<h1>Recordings</h1>");

      // Render the map
      var latlons = utils.modelsLatLons(self.recordings.models);
      var mapview = new MapView(null, {latlons: latlons});
      mapview.render();

      // Render the recordings list
      self.recordings.each(function(recording) {
        var view = new RecordingResultView(recording);
        $("#list").append(view.render());
      });
    }
  })
})