define([
  'backbone',
  'collections/SongsByShowCollection',
  'views/SongView',
  'views/MapView'
], function(Backbone, SongsByShowCollection, SongView, MapView){
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
      self.$el.html("<h1>Search</h1>");
      var mapview = new MapView();
      mapview.render();
      self.songs.each(function(song) {
        var view = new SongView(song, self.options);
        self.$el.append(view.render());
      });
    }
  })
})