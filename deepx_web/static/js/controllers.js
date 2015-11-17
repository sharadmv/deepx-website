app.controller('ProjectController', function ($scope, $window) {
});

app.controller('HomeCarouselController', function ($scope, $window) {
  $scope.interval = 5000;
  $scope.noWrapSlides = false;
  var slides = $scope.slides = [
    {
      image: '/img/space.jpg',
      text: 'Rethinking how machines learn'
    },
    {
      image: '/img/mountain-night.jpg',
      text: 'Redefining neural computation'
    },
    {
      image: '/img/mountains.jpg',
      text: 'Reaching new heights in scalability'
    },
    {
      image: '/img/nasa.jpg',
      text: 'Pushing the horizon of technology'
    },
  ];
});

app.controller('BeermindController', function ($scope, $window) {
  $scope.beermind = {
    name: "BeerMind",
    href: "beermind",
    backgroundImage: "/img/coffee.jpg"
  }
});

app.controller('SplashController', function() {

});

app.controller('PapersController', function ($scope, $window) {
});

app.controller('HomeController', function($scope, $window) {
  $scope.beermind = {
    name: "BeerMind",
    href: "beermind",
    backgroundImage: "/img/coffee.jpg"
  }
});
