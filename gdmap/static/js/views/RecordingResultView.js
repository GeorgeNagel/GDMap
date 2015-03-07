define([
  'underscore',
  'backbone',
  'mustache',
  'text!templates/recordingresult.mustache'
], function(_, Backbone, Mustache, recordingresulttemplate){
  "use strict";
  return Backbone.View.extend({
    initialize: function(model, options) {
        this.model = model;
        this.options = options;
    },
    render: function(){
      var modelJSON = _.clone(this.model.attributes);
      var rendered = Mustache.render(recordingresulttemplate, modelJSON);
      return rendered;
    }
  })
})