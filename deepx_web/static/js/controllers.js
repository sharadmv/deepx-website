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
    category: "Fruit / Vegetable Beer",
    temperature: 0.4
  }
  $scope.reviewText = "Press 'Generate' to create a review!"
  $scope.generate = function() {
    $http({
      url: "/api/beermind/generate",
      method: "GET",
      params: {
        category: $scope.data.category,
        rating: $scope.data.rating,
        temperature: $scope.data.categoryTemperature
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

app.controller('AboutController', function ($scope, $window) {
});

app.controller('SoftwareController', function ($scope, $window) {
  $scope.software = [
    {
        'name': 'deepx',
        'link': 'http://www.github.com/sharadmv/deepx',
        'description': 'A general purpose deep learning library that we use to train LSTMs and feed-forward networks.'
    },
    {
        'name': 'theanify',
        'link': 'http://www.github.com/sharadmv/theanify',
        'description': 'A decorator that allows you to naturally use theano in object-oriented code.'
    }
  ]
});

app.controller('HomeController', function($scope, $window) {
  $scope.projects = [
    {
      name: "BEERMIND",
      href: "home.beermind",
      backgroundImage: "/img/beer.jpg"
    },
  ];


  $scope.papers = [
    {
        name: 'Capturing Meaning in Product Reviews with Character-Level Generative Models',
        short: 'beermind',
        link: 'http://arxiv.org/abs/1511.03683',
        authors: 'Zachary C. Lipton, Sharad Vikram, Julian McAuley',
        other: 'Submitted to ICLR 2016 (arXiv 2015)',
    },
    {
        name: 'Learning to Diagnose with LSTM Recurrent Neural Networks',
        short: 'diagnose',
        link: 'http://arxiv.org/abs/1511.03677',
        authors: 'Zachary C. Lipton, David C. Kale, Charles Elkan, Randall Wetzell',
        other: 'Submitted to ICLR 2016 (arXiv 2015)',
    }
  ]
});
