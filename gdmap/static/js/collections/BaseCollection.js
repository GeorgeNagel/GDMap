define([
  'backbone',
], function(Backbone){
  "use strict";
  return Backbone.Collection.extend({
    parse_query_parameters: function(queryString) {
      // http://stackoverflow.com/questions/11671400/navigate-route-with-querystring
      var params = {};
        if(queryString){
          _.each(
            _.map(decodeURI(queryString).split(/&/g),function(el,i){
              var aux = el.split('='), o = {};
              if(aux.length >= 1){
                var val = undefined;
                if(aux.length == 2)
                  val = aux[1];
                o[aux[0]] = val;
              }
              return o;
            }),
            function(o){
              _.extend(params,o);
            }
          );
        }
        return params;
    }
  });
});

