require.config({
  paths: {
    jquery: "libs/jquery/jquery",
    underscore: "libs/underscore/underscore",
    backbone: "libs/backbone/backbone",
    async: "libs/requirejs-plugins/async",
    mustache: "libs/mustache/mustache",
    text: "libs/text/text",
    templates: "../templates"
  },
  shim: {
    backbone: {
      deps: ["jquery", "underscore"],
      exports: "Backbone"
    }
  }
});

require([
  "app"
], function(App) {
  "use strict";
  App.initialize();
});
