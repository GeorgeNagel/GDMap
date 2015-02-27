define([
  'backbone',
  'collections/SongsCollection',
  'views/SongView'
], function(Backbone, SongsCollection, SongView){
  "use strict";
  return Backbone.View.extend({
    el: $("#container"),
    initialize: function(options) {
      var self = this;
      self.options = options;
      var songs = new SongsCollection(options);
      songs.fetch({
        success: function() {
          self.render()
        }
      });
      this.songs = songs;
    },
    render: function(){
      var self = this;
      self.$el.html("<h1>Songs</h1>")
      self.songs.each(function(song) {
        var view = new SongView({model: song});
        self.$el.append(view.render());
      });
    }
  })
})