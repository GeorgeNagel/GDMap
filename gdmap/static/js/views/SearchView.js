define([
  'jquery',
  'backbone',
  'collections/SongsByShowCollection',
  'views/SongView',
  'views/MapView'
], function($, Backbone, SongsByShowCollection, SongView, MapView){
  "use strict";
  return Backbone.View.extend({
    el: $("#container"),
    initialize: function(options) {
      var self = this;
      self.options = options;
      var songs = new SongsByShowCollection([], options);
      songs.fetch({
        success: function() {
          self.render();
        }
      });
      this.songs = songs;
    },
    render: function(){
      var self = this;
      // Generate the list of lat-lons for the MapView to consume
      var latlons = [];
      $.each(self.songs.models, function(index, song) {
        var latlon = song.attributes.latlon.split(',');
        latlons.push(latlon);
      });
      self.$el.html("<h1>Search</h1>");
      var mapview = new MapView(null, {latlons: latlons});
      mapview.render();
      self.songs.each(function(song) {
        var view = new SongView(song, self.options);
        self.$el.append(view.render());
      });
    }
  })
})