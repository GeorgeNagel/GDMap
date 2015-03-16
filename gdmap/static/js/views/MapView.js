define([
  'backbone',
  'jquery',
  'async!https://maps.googleapis.com/maps/api/js?v=3.exp'
], function(Backbone, $){
  "use strict";
  return Backbone.View.extend({
    el: $("#map-canvas"),
    initialize: function(model, options) {
        this.songs = options.songs.models;
    },
    render: function(){
      var self = this;
      var myLatlng = new google.maps.LatLng(40,-80);
      var mapOptions = {
        zoom: 4,
        center: myLatlng
      }
      var map = new google.maps.Map(this.el, mapOptions);

      $.each(this.songs, function(index, song) {
        var latlon = song.attributes.latlon.split(',');
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