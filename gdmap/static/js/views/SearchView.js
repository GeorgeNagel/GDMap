define([
  'jquery',
  'backbone',
  'mustache',
  'collections/SongsByShowCollection',
  'views/SongView',
  'views/MapView',
  'text!templates/searchpage.mustache',
  'text!templates/searchwidget.mustache',
  'text!templates/filterwidgets.mustache',
  'text!templates/sortwidgets.mustache',
  'text!templates/paginatewidget.mustache',
  'utils',
], function($, Backbone, Mustache, SongsByShowCollection, SongView,
  MapView, searchpage, searchwidget, filterwidgets, sortwidgets, paginatewidget, utils){
  "use strict";
  return Backbone.View.extend({
    el: $("#content"),
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
      // Reset page number
      this.options.urlParams.page = 1;
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

      // Fill in the basic template on which to hang everything else
      self.$el.html(Mustache.render(searchpage));

      $("#menu").html("<h1>Search</h1>");

      // Render the map
      var latlons = utils.modelsLatLons(self.songs.models);
      var mapview = new MapView(null, {latlons: latlons});
      mapview.render();

      // Render the search widget
      var searchRendered = Mustache.render(searchwidget, {search_terms: this.options.urlParams.q});
      $("#search-bar").html(searchRendered);

      // Render the filter widgets
      var filterContext = {
        date_start: this.options.urlParams.date_gte,
        date_end: this.options.urlParams.date_lte
      }
      var filtersRendered = Mustache.render(filterwidgets, filterContext);
      $("#filters").html(filtersRendered);

      // Render the sort widgets
      var date_sort = this.options.urlParams.sort === "date";
      var relevance_sort = this.options.urlParams.sort === "relevance";
      var sort_asc = this.options.urlParams.sort_order === "asc";
      var sort_desc = this.options.urlParams.sort_order === "desc";
      var sort_context = {
        date_sort: date_sort,
        relevance_sort: relevance_sort,
        sort_asc: sort_asc,
        sort_desc: sort_desc
      }
      var sortRendered = Mustache.render(sortwidgets, sort_context);
      $("#sort").html(sortRendered);

      // Render the paginate widget
      var paginateContext = {
        prevPageExists: this.songs.hasPreviousPage(),
        nextPageExists: this.songs.hasNextPage()
      }
      var paginateRendered = Mustache.render(paginatewidget, paginateContext);
      $("#paginate").html(paginateRendered);

      // Render the songs list
      $("#list").html("");
      self.songs.each(function(song) {
        var view = new SongView(song, self.options);
        $("#list").append(view.render());
      });
    }
  })
})