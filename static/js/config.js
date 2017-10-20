//General configuration for modules
app.config(function(toastrConfig) {
    angular.extend(toastrConfig, {
      autoDismiss: false,
      containerId: 'toast-container',
      maxOpened: 0,    
      newestOnTop: true,
      positionClass: 'toast-bottom-center',
      preventDuplicates: false,
      preventOpenDuplicates: false,
      progressBar: true,
      target: 'body'
    });
  });