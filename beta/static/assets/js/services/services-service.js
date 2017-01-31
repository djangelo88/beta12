/**
 * Created by maykel on 19/01/17.
 */
app.factory('ServicesService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    //var _baseURL = 'http://app.caterfull.com:8000/api';
    var _getAll = function (model) {
        return $http.get(BASE_URL + 'services');
    };
    var _getMyWorkers = function (model) {
        return $http.get(BASE_URL + 'wservices');
    };


    var _getById = function (model, id) {
        return $http.get(BASE_URL + '?model=' + model + '&id=' + id);
    };

    var _post = function (object) {
        return $http.post(BASE_URL + 'services/add', object);
    };
    var _postEdit = function (id, object) {
        //console.log(id);
        return $http.post(BASE_URL + 'services/edit/' + id, object);
    };
    var _postDelete = function (objects) {
        return $http.post(BASE_URL + 'services/remove', objects);
    };



    return {
        getAll: _getAll,
        getMyWorkers:_getMyWorkers,
        getById: _getById,
        add: _post,
        edit: _postEdit,
        delete: _postDelete,
        baseUrl: BASE_URL
    };


}]);