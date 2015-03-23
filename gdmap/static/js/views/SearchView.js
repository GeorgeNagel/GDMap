define([
  'jquery',
  'backbone',
  'mustache',
  'collections/SongsByShowCollection',
  'views/SongView',
  'views/MapView',
  'text!templates/searchwidget.mustache',
  'text!templates/filtersortwidgets.mustache',
  'utils',
], function($, Backbone, Mustache, SongsByShowCollection, SongView,
  MapView, searchwidget, filtersortwidgets, utils){
  "use strict";
  return Backbone.View.extend({
    el: $("#container"),
    events: {
      "click .js-search-button": "updateSearchTerm",
      "keyup .js-search-input": "typeSearchTerm",
      "click .js-sort-date": "toggleSortDate",
      "click .js-sort-relevance": "toggleSortRelevance"
    },
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
    typeSearchTerm: function(e) {
      // Allow the user to type 'enter' to submit a new search
      if(e.keyCode == 13){
        this.updateSearchTerm();
      }
    },
    updateSearchTerm: function() {
      var self = this;
      var inputEl = $(".js-search-input");
      var searchText = inputEl.val();
      // Update the query parameters for the collection
      this.options.urlParams.q = searchText;
      this.navigateFromURLParams(this.options.urlParams);
    },
    toggleSortDate: function() {
      this.toggleSort('date', 'asc');
    },
    toggleSortRelevance: function() {
      // A higher relevance score is better, so sort in descending order
      this.toggleSort('relevance', 'desc');
    },
    toggleSort: function(sortField, defaultOrder) {
      // Toggle the sort order for a sort type and default order
      if (!('sort' in this.options.urlParams) || !('sort_order' in this.options.urlParams) || (this.options.urlParams.sort !== sortField)) {
        this.options.urlParams.sort = sortField;
        this.options.urlParams.sort_order = defaultOrder;
      } else {
        if (this.options.urlParams.sort_order === "asc") {
          this.options.urlParams.sort_order = "desc";
        } else {
          this.options.urlParams.sort_order = "asc";
        }
      }
      this.navigateFromURLParams(this.options.urlParams);
    },
    navigateFromURLParams: function(urlParams) {
      // Navigate to a new page given new url parameters
      var queryString = this.buildQuery(urlParams);
      var url = "/search/?" + queryString;
      // Don't listen to any more events for this view.
      this.undelegateEvents();
      this.options.router.navigate(url, {"trigger": true});
    },
    buildQuery: function(query_parameters) {
      var newQueryParameters = [];
      for (var key in query_parameters) {
        newQueryParameters.push(key + "=" + query_parameters[key]);
      }
      var newQuery = newQueryParameters.join("&");
      return newQuery;
    },
    render: function(){
      var self = this;

      self.$el.html("<h1>Search</h1>");

      // Render the map
      var latlons = utils.modelsLatLons(self.songs.models);
      var mapview = new MapView(null, {latlons: latlons});
      mapview.render();

      // Render the search widget
      var searchRendered = Mustache.render(searchwidget, {search_terms: this.options.urlParams.q});
      self.$el.append(searchRendered);
      // Render the filter widgets
      var filtersortRendered = Mustache.render(filtersortwidgets);
      self.$el.append(filtersortRendered);

      // Render the songs list
      self.songs.each(function(song) {
        var view = new SongView(song, self.options);
        self.$el.append(view.render());
      });
    }
  })
})