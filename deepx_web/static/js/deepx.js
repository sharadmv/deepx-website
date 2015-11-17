var app = angular.module('deepx', ['ui.bootstrap', 'ui.router', 'ngAnimate']);

app.directive("deepxProject", function() {
  return {
    restrict: 'E',
    scope: {
        project: "=project"
    },
    transclude: true,
    templateUrl: "/templates/deepx-project.html",
    link: function(scope, element, attrs) {
    }
  }
});
