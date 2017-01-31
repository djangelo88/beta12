/**
 * Created by maykel on 23/01/17.
 */

app.controller('RecipesController', ['$scope', '$window', '$aside', 'PlaceholderTextService', '$alert', '$http', 'RecipesService','IngredientsService', '$timeout','$location','AlertConfirmService','NotificationService', function ($scope, $window, $aside, PlaceholderTextService, $alert, $http, RecipesService,IngredientsService, $timeout,$location,AlertConfirmService,NotificationService) {

    // settings
    $scope.settings = {
        singular: 'Receta',
        plural: 'Recetas',
        cmd: 'Nuevo'
    };
    //page
    $scope.page = {
        title: 'Recetas',
        description: 'In most applications you need basic table listings and editing capabilities.' +
        ' With this app you can create simple admin functionality based on a json web service.',
        icon: 'md md-group'
    };


    //console.debug($hh);

    // adding customers data
    var data = [];
    RecipesService.getAll()
        .success(function (data, status, headers, config) {
            console.log(data);
            $scope.data = data;
        });
    IngredientsService.getAll().success(function (data) {
        console.log(data);
        $scope.ingredients = data;
    });

    $scope.checkIngredient = function (item, ing, event) {
        event.stopPropagation();

        var index= (item.ingredients.indexOf(ing));
        console.log(index);
        console.log(ing.selected);
        if(index > -1 && ing.selected === false){

            console.log(ing.selected);
            item.ingredients.pop(ing);
        }else if(index === -1 && ing.selected === true){
            ing.cant = null;
            item.ingredients.push(ing);
        }

        //worker.selected = !worker.selected;
    }

    //adding others stuffs

    // defining template
    var formTpl = $aside({
        scope: $scope,
        templateUrl: '/static/assets/tpl/recipes/recipes-form.html',
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

    $scope.addWorkers = function(){
        angular.element('.tooltip').remove();
        otherformTpl.show();
        // if (data) {
        //    console.log(data);
        //    //item.editing = true;
        //    //$scope.item = item;
        //    $scope.settings.cmd = 'AddWorker';
        //    showForm();
        //}
    }

    $scope.editItem = function (item) {

        if (item) {
            console.log(item);
            item.editing = true;
            $scope.item = item;
            $scope.settings.cmd = 'Edit';

            //console.log($scope.item);
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
            //icon: PlaceholderTextService.createIcon(true),
            editing: true,
            creating: true,
            name: '',
            description: '',
            ingredients: []

        };
        $scope.item = item;
        $scope.settings.cmd = 'New';

        showForm();
    };

    $scope.saveItem = function (item, saveAndAdd) {

        console.log(item.ingredients);

        $scope.validation_errors = '';

        if ($scope.settings.cmd == 'New') {

            RecipesService.add($scope.item)
                .success(function (data_) {
                    var refererNotThemeforest = $alert({
                        title: '',
                        content: 'Se ha creado el ingrediente satisfactoriamente',
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
                        console.log('kk');
                        console.log(data);
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
                        content: 'Ha exixtido un error al adicionar el ingrediente',
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

            RecipesService.edit($scope.item.id, $scope.item)
                .success(function (data) {

                    NotificationService.success('', 'Se ha actualizado el ingrediente');
                    hideForm();

                }).error(function (data) {

                    $scope.validation_errors = JSON.parse(data);
                    NotificationService.error('Error', 'Ha existido un error al adicionar el ingrediente');

                });
        }


    };

   $scope.remove = function (item) {

        if (item) {
            callbackFn = function () {
                RecipesService.delete(new Array(item))
                    .success(function () {
                        NotificationService.success('', 'Se ha eliminado el ingrediente seleccionado');
                        $scope.data.splice($scope.data.indexOf(item), 1);
                    }).error(function () {
                        NotificationService.error('Error', 'Ha existido un error al eliminar el ingrediente seleccionado');
                    });
            };

            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea eliminar el ingrediente seleccionado?", callbackFn);

        } else {

            callbackFn = function () {
                var seleccionados = $scope.data.filter(
                    function (item) {
                        return item.selected;
                    }
                );
                RecipesService.delete(seleccionados).success(function () {
                    NotificationService.success('', 'Se han eliminado los ingredientes seleccionados');

                    for (index in seleccionados) {
                        $scope.data.splice($scope.data.indexOf(seleccionados[index]), 1);
                    }
                }).error(function () {
                    NotificationService.error('Error', 'Ha existido un error al eliminar los ingredientes seleccionados');
                });
            }
            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea los ingredientes seleccionados?", callbackFn);
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

