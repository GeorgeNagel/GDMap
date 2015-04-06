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
        // Extend the bounds to include each marker's position
        bounds.extend(marker.position);
      });

      // Now fit the map to the newly inclusive bounds
      map.fitBounds(bounds);
      // Set a max zoom level after the map is done scaling
      var listener = google.maps.event.addListener(map, "idle", function () {
        var currentZoom = map.getZoom();
        var maxZoom = 5;
        if (currentZoom > maxZoom) {
          map.setZoom(maxZoom);
        }
        google.maps.event.removeListener(listener);
      });
    }
  })
})