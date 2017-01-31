/**
 * Created by Hector on 25/01/2017.
 */

app.factory('WebsiteService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    //var _baseURL = 'http://app.caterfull.com:8000/api';
    var _getAll = function (model) {
        return $http.get(BASE_URL + 'allwebsitedata');
    };


    var _getWebsite = function () {
        return {
            template: {
                id: 1,
                name: 'Template # 1',
                description: 'I am a very simple card. I am good at containing small bits of information. I am convenient' +
                'because I require little markup to use effectively.',
                selected: false
            },
            basic_info: {
                name: 'Clientes',
                description: 'I am a very simple card. I am good at containing small bits of information. I am convenient' +
                'because I require little markup to use effectively.',
                logo: ''
            },
            gallery: {
                comments: 'In most applications you need basic table listings and editing capabilities.' +
                ' With this app you can create simple admin functionality based on a json web service.',
                images: [
                    {
                        image: '',
                        name: '',
                        description: '',
                        background: false
                    }
                ]
            },
            menu: [{
                image: '',
                name: '',
                description: ''
            }],
            social_networks: {
                twitter: 'http://www.twitter.com/user_page',
                instagram: 'http://www.instagram.com/user_page',
                facebook: 'http://www.facebook.com/user_page',
                yelp: 'http://www.yelp.com/user_page',
                gplus: 'http://www.gplus.com/user_page'
            },
            contact_info: {
                phone: '',
                email: '',
                address: {}
            },
            staff: []
        };
    }

    var _getById = function (model, id) {
        return $http.get(BASE_URL + '?model=' + model + '&id=' + id);
    };
    var _postphoto = function (id, object) {
        return $http.post(BASE_URL+'photogallerysave' + id, object);
    };
    var _post = function (model, object) {
        return $http.post(BASE_URL + model, object);
    };
    var _postEdit = function (model, id, object) {
        return $http.post(BASE_URL + model + id, object);
    };
    var _postDelete = function (model, objects) {
        return $http.post(BASE_URL + model + '/delete', objects);
    };
    //var _createIcon = function (object) {
    //
    //    if (object.new) {
    //        return '<i class="fa fa-user  light-green lighten-1 icon-color"></i>';
    //    }
    //    return '<i class="fa fa-user  grey lighten-1 icon-color"></i>';
    //
    //}


    return {
        getAll: _getAll,
        getWebsite: _getWebsite,
        getById: _getById,
        postphoto:_postphoto,
        add: _post,
        edit: _postEdit,
        delete: _postDelete,
        //createIcon: _createIcon,
        baseUrl: BASE_URL
    };


}]);