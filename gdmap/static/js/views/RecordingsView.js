define([
  'backbone',
  'collections/RecordingsCollection',
  'views/RecordingResultView'
], function(Backbone, RecordingsCollection, RecordingResultView){
  "use strict";
  return Backbone.View.extend({
    el: $("#container"),
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
      self.$el.html("<h1>Recordings</h1>")
      self.recordings.each(function(recording) {
        var view = new RecordingResultView(recording);
        self.$el.append(view.render());
      });
    }
  })
})