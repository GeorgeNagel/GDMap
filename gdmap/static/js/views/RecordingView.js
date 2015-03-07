define([
  'backbone',
  'mustache',
  'text!templates/recording.mustache'
], function(Backbone, Mustache, recordingtemplate){
  "use strict";
  return Backbone.View.extend({
    el: $("#container"),
    initialize: function(options) {
      this.showID = options.show_id;
    },
    render: function(){
      var self = this;
      self.$el.html("<h1>Recording</h1>");
      var rendered = Mustache.render(recordingtemplate, {show_id: this.showID});
      self.$el.append(rendered);
    }
  })
})