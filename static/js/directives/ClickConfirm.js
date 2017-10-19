//Simple directive used to confirm an ng-click action
//usage: <button ng-click="clickFunction()" click-confirm="Are you sure?"></button>
app.directive('clickConfirm', [
    function(){
      return {
        priority: -1,
        restrict: 'A',
        link: function(scope, element, attrs) {
          element.bind('click', function(e) {

            var message = attrs.clickConfirm;

            if(message && !confirm(message)) {
              e.stopImmediatePropagation();
              e.preventDefault();
            }

          });
        }
      }
    }
  ]);