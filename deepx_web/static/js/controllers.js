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
        temperature: $scope.data.temperature
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
    {
      name: "DDC",
      href_absolute: "/ddc",
      backgroundImage: "/img/ddc.jpg"
    },
    {
      name: "SDGAN",
      href_absolute: "https://chrisdonahue.github.io/sdgan/",
      backgroundImage: "/img/sdgan.jpg"
    },
    {
      name: "WaveGAN",
      href_absolute: "http://wavegan-v1.s3-website-us-east-1.amazonaws.com",
      backgroundImage: "/img/wavegan.jpg"
    },
  ];


  $scope.papers = [
    {
        name: 'Synthesizing Audio with Generative Adversarial Networks',
        short: 'wavegan',
        link: 'https://arxiv.org/abs/1802.04208',
        authors: 'Chris Donahue, Julian McAuley, Miller Puckette'
    },
    {
        name: 'Semantically Decomposing the Latent Spaces of Generative Adversarial Networks',
        short: 'sdgan',
        link: 'https://arxiv.org/abs/1705.07904',
        authors: 'Chris Donahue, Zachary C. Lipton, Akshay Balsubramani, Julian McAuley'
    },
    {
        name: 'Dance Dance Convolution',
        short: 'ddc',
        link: 'https://arxiv.org/abs/1703.06891',
        authors: 'Chris Donahue, Zachary C. Lipton, Julian McAuley'
    },
    {
        name: 'The Mythos of Model Interpretability',
        short: 'clinical',
        link: 'https://arxiv.org/abs/1606.03490',
        authors: 'Zachary C. Lipton',
        other: 'ICML Workshop on Human Interpretability of Machine Learning (WHI) 2016',
    },
    {
        name: 'Directly Modeling Missing Data in Sequences with RNNs: Improved Classification of Clinical Time Series',
        short: 'clinical',
        link: 'https://arxiv.org/abs/1606.04130',
        authors: 'Zachary C. Lipton, David C. Kale, Randall Wetzel',
        other: 'Machine Learning for Health Care (MLHC) 2016 / JMLR',
    },
    {
        name: 'Context Matters: Refining Object Detection in Video with Recurrent Neural Networks',
        short: 'context',
        link: 'http://arxiv.org/abs/1607.04648',
        authors: 'Subarna Tripathi, Zachary C. Lipton, Serge Belongie, Truong Nguyen',
        other: 'British Machine Vision Converence (BMVC) 2016',
    },
    {
        name: 'Capturing Meaning in Product Reviews with Character-Level Generative Models',
        short: 'beermind',
        link: 'http://arxiv.org/abs/1511.03683',
        authors: 'Zachary C. Lipton, Sharad Vikram, Julian McAuley',
        other: '',
    },
    {
        name: 'Learning to Diagnose with LSTM Recurrent Neural Networks',
        short: 'diagnose',
        link: 'http://arxiv.org/abs/1511.03677',
        authors: 'Zachary C. Lipton, David C. Kale, Charles Elkan, Randall Wetzell',
        other: 'ICLR 2016',
    },
  ]
});
