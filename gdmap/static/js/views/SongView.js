define([
  'underscore',
  'backbone',
  'mustache',
  'text!templates/song.mustache'
], function(_, Backbone, Mustache, songtemplate){
  "use strict";
  return Backbone.View.extend({
    render: function(){
      var rendered = Mustache.render(songtemplate, this.model.toJSON());
      return rendered;
    }
  })
})