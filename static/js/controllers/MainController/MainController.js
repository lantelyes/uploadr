app.controller("MainController", function($scope, $http){ 

    $scope.fileList = [];



    init = function()  {

// Simple GET request example:
    $http({
        method: 'GET',
        url: '/list'
    }).then(function successCallback(response) {

            $scope.fileList = response.data;

        }, function errorCallback(response) {

        });

    }


    init();

});