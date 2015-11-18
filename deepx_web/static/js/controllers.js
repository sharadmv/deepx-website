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

app.controller('BeermindController', function ($scope, $http) {

  $scope.data = {
    rating: 5.0,
    ratingTemperature: 0.7,
    category: "Fruit / Vegetable Beer",
    categoryTemperature: 0.7
  }
  $scope.reviewText = "Press 'Generate' to create a review!"
  $scope.generateCategory = function() {
    $http({
      url: "/api/beermind/generate_category",
      method: "GET",
      params: {
        category: $scope.data.category,
        temperature: $scope.data.categoryTemperature
      }
    }).then(function(result) {
      $scope.reviewText = result.data.results;
    });
  }
  $scope.generateRating = function() {
    $http({
      url: "/api/beermind/generate_rating",
      method: "GET",
      params: {
        rating: $scope.data.rating,
        temperature: $scope.data.ratingTemperature
      }
    }).then(function(result) {
      $scope.reviewText = result.data.results;
    });
  }
});

app.controller('SplashController', function() {

});

app.controller('PapersController', function ($scope, $window) {
});

app.controller('HomeController', function($scope, $window) {
  $scope.beermind = {
    name: "BEERMIND",
    href: "home.beermind",
    backgroundImage: "/img/beer.jpg"
  }
});
