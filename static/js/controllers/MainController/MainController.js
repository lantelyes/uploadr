app.controller("MainController", function($scope, $http, Upload, toastr){ 

    //Options for the search dialog
    $scope.searchOptions = {
        query: "",
        extentions: {
            word: false,
            pdf: false
        },
        types: {
            name: true,
            contents: false,
        },
        caseSensitive: false
    };

    $scope.fileList = [];
    $scope.isSearching = false;

    //Open the descripion editor
    $scope.editFileDescription = function(file) {
        file.isEditingDescription = true;
    }

    //Toggle the search window
    $scope.toggleSearch = function() {
        $scope.isSearching = !$scope.isSearching;
    }

    //Get the download link for a given file
    $scope.getDownloadLink = function(file) {
        
        return API.DOWNLOAD.URL + file.name + "." + file.extention;
        
    }

    //Given a file object, return the appropriate icon class for use in the DOM
    $scope.getFileIcon = function(file) {
        
                switch(file.extention){
                    case "doc":
                    case "docx":
                        return "fa-file-word-o"
                    case "pdf":
                        return "fa-file-pdf-o"
                    default:
                        return "fa-file"
                }
        
            }
        
            //Given a file object, return its type based on its extention
            $scope.getFileType = function(file) {
        
                switch(file.extention){
                    case "doc":
                    case "docx":
                        return "Word Document"
                    case "pdf":
                        return "PDF"
                    default:
                        return "Unknown"
                }
        
            }
            

    //Upload the selected file to the server
    $scope.upload= function($file) {
         Upload.upload({
            url: API.UPLOAD.URL,
            data: {file: $file},
        }).then(function (response) {
            toastr.success("Upload Successful");
            populateFileList();
        }, function (response) {
            toastr.error(response.data.message);
        });
    }

    //Upload the selected file to the server
    $scope.delete = function(file) {
        $http({
            method: API.DELETE.METHOD,
            url: API.DELETE.URL + file["_id"]
        }).then(function successCallback(response) {
    
                populateFileList();
    
            }, function errorCallback(response) {
                toastr.error(response.data.message);
        });
    }
    
    //Updatethe file descripion on the server
    $scope.saveFileDescription = function(file) {

        $http({
            method: API.UPDATE.METHOD,
            url: API.UPDATE.URL,
            data: file
        }).then(function successCallback(response) {
                toastr.success("Succesfily saved file desciption");
                file.isEditingDescription = false
            }, function errorCallback(response) {
                toastr.error(response.data.message);
        });

    }

    //Search files using the saved search paramaters
    $scope.searchFiles = function(searchOptions)
    {

        queryString = buildQueryString(searchOptions);
        $http({
            method: API.LIST.METHOD,
            url: API.LIST.URL + queryString,
        }).then(function successCallback(response) {
                $scope.fileList = response.data;
                $scope.isSearching = true;
            }, function errorCallback(response) {
                toastr.error(response.data.message);
        });
    }

    //Controller initialization
    init = function()  {
        populateFileList();

        //Initialize bootstrap popovers
        $(function () {
            $('[data-toggle="popover"]').popover()
        })

    }



    //Build a query string to pass to the API for file searching
    buildQueryString = function(searchOptions) {
        queryString =  "query="+searchOptions.query + "&";

        if(searchOptions.extentions.word)
        {
            queryString += "ext=doc&ext=docx&"
        }
        if(searchOptions.extentions.pdf)
        {
            queryString += "ext=pdf&"
        }
        if(searchOptions.types.name)
        {
            queryString += "type=name&"
        }
        if(searchOptions.types.contents)
        {
            queryString += "type=contents&"
        }
        if(searchOptions.caseSensitive)
        {
            queryString += "case=true"
        }

        return queryString;
    }


    //populate the file list with data from the server
    populateFileList = function() {
        $http({
            method: 'GET',
            url: '/list?query=&ext=pdf&ext=doc&ext=docx'
        }).then(function successCallback(response) {
    
                $scope.fileList = response.data;
    
            }, function errorCallback(response) {
                toastr.error(response.data.message);
        });
    }

    init();
});


