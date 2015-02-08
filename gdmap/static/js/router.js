// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'views/IndexView'
], function($, _, Backbone, IndexView){
  var AppRouter = Backbone.Router.extend({
    routes: {
      // Define some URL routes
      '': 'index',

      // Default
      '*actions': 'defaultAction'
    },
    index: function() {
      var indexView = new IndexView();
      indexView.render(); 
    },
    defaultAction: function(actions) {
        console.log('No route:', actions);
    }
  });

  var initialize = function(){
    var app_router = new AppRouter();
    Backbone.history.start();
  };
  return {
    initialize: initialize
  };
});