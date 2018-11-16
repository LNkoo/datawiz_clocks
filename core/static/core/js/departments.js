$(document).ready(function () {
    var storeModel = {
        departments: ko.observableArray([]),
        showDepartments: ko.observable(true),
        groupOfProducts: ko.observableArray([]),
        showGroupOfProducts: ko.observable(false),
        products: ko.observableArray([]),
        showProducts: ko.observable(false),
        uploadItems: uploadItems,
        undo: undo,
        redo: redo,
    };
    ko.applyBindings(storeModel, $('.store')[0]);

    $.ajax({
        url: "/api/departments/",
        context: document.body
    }).done(function (data) {
        storeModel.departments(data);
    });

    function uploadItems(item) {
        if (item.groups_url) {
            $.ajax({
                url: item.groups_url,
                context: document.body
            }).done(function (data) {
                storeModel.groupOfProducts(data);
                storeModel.showDepartments(false);
                storeModel.showGroupOfProducts(true);
            })
        } else if (item.products_url) {
            $.ajax({
                url: item.products_url,
                context: document.body
            }).done(function (data) {
                storeModel.products(data.results);
                storeModel.showGroupOfProducts(false);
                storeModel.showProducts(true);
            })
        }
    }

    function undo() {
        if (storeModel.showGroupOfProducts()) {
            storeModel.showGroupOfProducts(false);
            storeModel.showDepartments(true);
        } else if (storeModel.showProducts) {
            storeModel.showProducts(false);
            storeModel.showGroupOfProducts(true);
        }
    }

    function redo() {
        if (storeModel.showGroupOfProducts() && storeModel.products().length>0) {
            storeModel.showGroupOfProducts(false);
            storeModel.showProducts(true);
        } else if (storeModel.showDepartments() && storeModel.groupOfProducts().length>0) {
            storeModel.showDepartments(false);
            storeModel.showGroupOfProducts(true);
        }
    }
});


