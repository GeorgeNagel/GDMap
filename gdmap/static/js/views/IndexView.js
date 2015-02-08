define([
  'backbone'
], function(Backbone){
  "use strict";
  return Backbone.View.extend({
    el: $("#container"),
    render: function(){
        this.$el.html("<h1>Booger</h1>")
    }
  });
});