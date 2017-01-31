/**
 * Created by Hector on 12/01/2017.
 */
app.factory('CalendarService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    //var _baseURL = 'http://app.caterfull.com:8000/api';
    var local_model = 'events';
    var _events = function (model) {
        return $http.get(BASE_URL + local_model);
    };

    var _postDelete = function (objects) {
        return $http.post(BASE_URL + local_model + '/delete', objects);
    };

    var _createIcon = function (status) {

        switch (status) {
            case 2:
                return '<i class="md md-mode-edit blue lighten-1 icon-color"></i>';
                break;
            case 1:
                return '<i class="md md-query-builder orange lighten-1 icon-color"></i>';
                break;
            case 3:
                return '<i class="md md-done light-green lighten-1 icon-color"></i>';
                break;
            //case 4:
            //  return  '<i class="md md-report deep-orange lighten-1 icon-color"></i>';
            //   break;
            case 4:
                return '<i class="md md-clear red accent-3 icon-color"></i>';
                break;
            default :
                return '<i class="md md-assignment grey lighten-1 icon-color"></i>';
        }

    }
    //var _formatedEvents = function () {
    //    _events(local_model).success(function (data) {
    //        console.log(data)
    //        data.each(function (event) {
    //            //console.debug(event);
    //
    //        })
    //    });
    //    //events.each(function(event){
    //    //    console.debug(event);
    //    //})
    //
    //
    //};


    return {
        getAllEvents: _events,
        createIcon: _createIcon,
        delete: _postDelete,
        baseUrl: BASE_URL
        //calendarEvents: _formatedEvents
    };


}]);
