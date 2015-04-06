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

      // Track the bounds of the markers
      // http://stackoverflow.com/questions/15719951/google-maps-api-v3-auto-center-map-with-multiple-markers
      var bounds = new google.maps.LatLngBounds();

      $.each(this.latlons, function(index, latlon) {
        var position = new google.maps.LatLng(latlon[0], latlon[1]);
        var marker = new google.maps.Marker({
            position: position,
            map: map,
            title: 'Hello World!'
        });
        //extend the bounds to include each marker's position
        bounds.extend(marker.position);
      });

      //now fit the map to the newly inclusive bounds
      map.fitBounds(bounds);
    }
  })
})