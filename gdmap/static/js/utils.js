define([
  'jquery'
], function($) {
  "use strict";
  return {
    modelsLatLons: function(modelsArray) {
      // Return an array of [latitude, longitude] arrays
      // given an array of models with a latlon key
      var latlons = [];
      $.each(modelsArray, function(index, song) {
        var latlon = song.attributes.latlon.split(',');
        latlons.push(latlon);
      });
      return latlons;
    }
  };
});