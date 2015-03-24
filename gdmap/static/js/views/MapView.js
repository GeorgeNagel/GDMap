define([
  'backbone',
  'jquery',
  'async!https://maps.googleapis.com/maps/api/js?v=3.exp'
], function(Backbone, $){
  "use strict";
  return Backbone.View.extend({
    el: "#map",
    initialize: function(model, options) {
        this.latlons = options.latlons;
    },
    render: function(){
      var self = this;
      var centerLatlng = new google.maps.LatLng(41,-98);
      var mapOptions = {
        zoom: 3,
        center: centerLatlng
      }
      var map = new google.maps.Map(this.el, mapOptions);

      $.each(this.latlons, function(index, latlon) {
        var position = new google.maps.LatLng(latlon[0], latlon[1]);
        var marker = new google.maps.Marker({
            position: position,
            map: map,
            title: 'Hello World!'
        });
      });
    }
  })
})