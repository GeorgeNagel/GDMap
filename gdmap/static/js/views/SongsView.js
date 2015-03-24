define([
  'backbone',
  'mustache',
  'collections/SongsCollection',
  'views/SongView',
  'views/MapView',
  'text!templates/listpage.mustache',
  'utils'
], function(Backbone, Mustache, SongsCollection, SongView, MapView, listpage, utils){
  "use strict";
  return Backbone.View.extend({
    el: $("#content"),
    initialize: function(options) {
      var self = this;
      var songs = new SongsCollection([], options);
      songs.fetch({
        success: function() {
          self.render()
        }
      });
      this.songs = songs;
    },
    render: function(){
      var self = this;
      // Render the base template
      var pageRendered = Mustache.render(listpage);
      self.$el.html(pageRendered);

      $("#menu").html("<h1>Songs</h1>");

      // Render the map
      var latlons = utils.modelsLatLons(self.songs.models);
      var mapview = new MapView(null, {latlons: latlons});
      mapview.render();

      // Render the songs list
      self.songs.each(function(song) {
        var view = new SongView(song);
        $("#list").append(view.render());
      });
    }
  })
})