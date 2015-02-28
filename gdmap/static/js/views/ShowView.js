define([
  'backbone',
  'mustache',
  'text!templates/show.mustache'
], function(Backbone, Mustache, showtemplate){
  "use strict";
  return Backbone.View.extend({
    el: $("#container"),
    initialize: function(options) {
      this.showID = options.show_id;
    },
    render: function(){
      var self = this;
      self.$el.html("<h1>Show</h1>");
      var rendered = Mustache.render(showtemplate, {show_id: this.showID});
      self.$el.append(rendered);
    }
  })
})