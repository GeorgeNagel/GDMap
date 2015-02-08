require.config({
  paths: {
    jquery: 'libs/jquery/jquery',
    underscore: 'libs/underscore/underscore',
    backbone: 'libs/backbone/backbone',
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
