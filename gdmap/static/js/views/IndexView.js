define([
  'backbone'
], function(Backbone){
  "use strict";
  return Backbone.View.extend({
    el: $("#content"),
    render: function(){
        this.$el.html("<h1>Index</h1>")
    }
  });
});