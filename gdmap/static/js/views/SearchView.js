define([
  'jquery',
  'backbone',
  'mustache',
  'collections/SongsByShowCollection',
  'views/SongView',
  'views/MapView',
  'text!templates/searchwidget.mustache',
  'text!templates/filtersortwidgets.mustache',
  'text!templates/paginatewidget.mustache',
  'utils',
], function($, Backbone, Mustache, SongsByShowCollection, SongView,
  MapView, searchwidget, filtersortwidgets, paginatewidget, utils){
  "use strict";
  return Backbone.View.extend({
    el: $("#container"),
    events: {
      "click .js-search-button": "updateSearchTerms",
      "click .js-sort-date": "toggleSortDate",
      "click .js-sort-relevance": "toggleSortRelevance",
      "click .js-page-prev": "previousPage",
      "click .js-page-next": "nextPage",
      "keyup .js-search-input": "typeSearchTerm",
      "keyup .js-filter-date-start": "typeSearchTerm",
      "keyup .js-filter-date-end": "typeSearchTerm",
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
        this.updateSearchTerms();
      }
    },
    updateSearchTerms: function() {
      var self = this;
      // Update the phrase search terms
      var inputEl = $(".js-search-input");
      var searchText = inputEl.val();
      this.options.urlParams.q = searchText;
      // Update the start date filter
      var dateStartEl = $(".js-filter-date-start");
      var dateStartText = dateStartEl.val();
      this.options.urlParams.date_gte = dateStartText;
      // Update the end date filter
      var dateEndEl = $(".js-filter-date-end");
      var dateEndText = dateEndEl.val();
      this.options.urlParams.date_lte = dateEndText;
      // Navigate to the new URL
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
    previousPage: function() {
      // Paginate backwards through results
      var currentPage = 1;
      if ('page' in this.options.urlParams) {
        // Cast the page url parameter to an int
        currentPage = Math.floor(this.options.urlParams.page);
      }
      var previousPage = currentPage - 1;
      if (previousPage < 1) {
        previousPage = 1;
      }
      this.options.urlParams.page = previousPage;
      this.navigateFromURLParams(this.options.urlParams);
    },
    nextPage: function() {
      // Paginate through results
      var currentPage = 1;
      if ('page' in this.options.urlParams) {
        // Cast the page url parameter to an int
        currentPage = Math.floor(this.options.urlParams.page);
      }
      var nextPage = currentPage + 1;
      this.options.urlParams.page = nextPage;
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
      var filterContext = {
        date_start: this.options.urlParams.date_gte,
        date_end: this.options.urlParams.date_lte
      }
      var filtersortRendered = Mustache.render(filtersortwidgets, filterContext);
      self.$el.append(filtersortRendered);

      // Render the paginate widget
      var paginateContext = {
        prevPageExists: this.songs.hasPreviousPage(),
        nextPageExists: this.songs.hasNextPage()
      }
      var paginateRendered = Mustache.render(paginatewidget, paginateContext);
      self.$el.append(paginateRendered);

      // Render the songs list
      self.songs.each(function(song) {
        var view = new SongView(song, self.options);
        self.$el.append(view.render());
      });
    }
  })
})