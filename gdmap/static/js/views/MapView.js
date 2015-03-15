define([
  'backbone',
  'async!https://maps.googleapis.com/maps/api/js?v=3.exp'
], function(Backbone){
  "use strict";
  return Backbone.View.extend({
    el: $("#map-canvas"),
    initialize: function(options) {},
    render: function(){
      var self = this;
      var myLatlng = new google.maps.LatLng(-25.363882,131.044922);
      var mapOptions = {
        zoom: 4,
        center: myLatlng
      }
      var map = new google.maps.Map(this.el, mapOptions);

      var marker = new google.maps.Marker({
          position: myLatlng,
          map: map,
          title: 'Hello World!'
      });
    }
  })
})