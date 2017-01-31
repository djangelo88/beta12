/**
 * Created by maykel on 26/01/17.
 */
app.controller('ProductController', ['$scope', '$window', '$aside', 'PlaceholderTextService', '$alert', '$http', 'ProductService', '$timeout','$location','AlertConfirmService','NotificationService', function ($scope, $window, $aside, PlaceholderTextService, $alert, $http, ProductService, $timeout,$location,AlertConfirmService,NotificationService) {
    // settings
    $scope.settings = {
        singular: 'Producto',
        plural: 'Productos',
        cmd: 'Nuevo'
    };
    //page
    $scope.page = {
        title: 'Productos',
        description: 'In most applications you need basic table listings and editing capabilities.' +
        ' With this app you can create simple admin functionality based on a json web service.',
        icon: 'md md-local-pizza'
    };

    // adding customers data
    ProductService.getAll()
        .success(function (data, status, headers, config) {
            $scope.data = data;
        });

    //adding others stuffs

    // defining template
    var formTpl = $aside({
        scope: $scope,
        templateUrl: '/static/assets/tpl/products/products-form.html',
        show: false,
        placement: 'left',
        backdrop: false,
        animation: 'am-slide-left'
    });

    // methods
    $scope.checkAll = function () {
        angular.forEach($scope.data, function (item) {
            item.selected = !item.selected;
        });
    };


    $scope.editItem = function (item) {

        if (item) {
            item.editing = true;
            $scope.item = item;
            $scope.settings.cmd = 'Edit';
            showForm();
        }
    };

    $scope.viewItem = function (item) {
        if (item) {
            item.editing = false;
            $scope.item = item;
            $scope.settings.cmd = 'View';
            showForm();
        }
    };

    $scope.createItem = function () {

        var item = {
            editing: true,
            creating: true,
            name: '',
            description: '',
            tarifa_horaria: '',
            workers: $scope.data1

        };

        $scope.item = item;
        $scope.settings.cmd = 'New';

        showForm();
    };

    $scope.saveItem = function (item, saveAndAdd) {

        $scope.validation_errors = '';

        if ($scope.settings.cmd == 'New') {
            //
            var select= $scope.data1.filter(
                    function (item) {
                        return item.selected;
                    }
                );
                console.log($scope.data1);
                console.log(select);

            ProductService.add($scope.item)
                .success(function (data_) {
                    var refererNotThemeforest = $alert({
                        title: '',
                        content: 'Se ha creado el servicio satisfactoriamente',
                        placement: 'top-right',
                        type: 'success',
                        //types:info,theme,danger,success,warning
                        //container: '.alert-container-top-right',
                        show: true,
                        animation: 'mat-grow-top-right'
                    });

                    $timeout(function () {
                        refererNotThemeforest.show();
                    }, 1750);


                    if ($scope.settings.cmd == 'New') {
                        $scope.data.push(data_);
                    }

                    hideForm();

                    if (saveAndAdd) {
                    $scope.createItem();
                    }
                }).error(function (data) {

                    $scope.validation_errors = JSON.parse(data);
                    var refererNotThemeforest = $alert({
                        title: 'Error',
                        content: 'Ha exixtido un error al adicionar el servicio',
                        placement: 'top-right',
                        type: 'danger',
                        //types:info,theme,danger,success,warning
                        //container: '.alert-container-top-right',
                        show: true,
                        animation: 'mat-grow-top-right'
                    });
                    $timeout(function () {
                        refererNotThemeforest.show();
                    }, 1750);

                });
        } else {

            ProductService.edit($scope.item.id, $scope.item)
                .success(function (data) {

                    NotificationService.success('', 'Se ha actualizado el servicio');
                    hideForm();

                }).error(function (data) {

                    $scope.validation_errors = JSON.parse(data);
                    NotificationService.error('Error', 'Ha existido un error al adicionar el servicio');

                });
        }


    };

   $scope.remove = function (item) {

        if (item) {
            callbackFn = function () {
                ProductService.delete(new Array(item))
                    .success(function () {
                        NotificationService.success('', 'Se ha eliminado el servicio seleccionado');
                        $scope.data.splice($scope.data.indexOf(item), 1);
                    }).error(function () {
                        NotificationService.error('Error', 'Ha existido un error al eliminar el servicio seleccionado');
                    });
            };

            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea eliminar el servicio seleccionado?", callbackFn);

        } else {

            callbackFn = function () {
                var seleccionados = $scope.data.filter(
                    function (item) {
                        return item.selected;
                    }
                );
                ProductService.delete(seleccionados).success(function () {
                    NotificationService.success('', 'Se han eliminado los servicio seleccionados');

                    for (index in seleccionados) {
                        $scope.data.splice($scope.data.indexOf(seleccionados[index]), 1);
                    }
                }).error(function () {
                    NotificationService.error('Error', 'Ha existido un error al eliminar los servicios seleccionados');
                });
            }
            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea los servicios seleccionados?", callbackFn);
        }


    };

    showForm = function () {
        angular.element('.tooltip').remove();
        formTpl.show();
    };

    hideForm = function () {
        formTpl.hide();
    };

    $scope.$on('$destroy', function () {
        hideForm();
    });

    $scope.print = function () {
        return $window.print();
    }


}]);


