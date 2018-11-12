$(document).ready(function () {
    var departmentModel = {departments: ko.observableArray([])};
    ko.applyBindings(departmentModel, $('.departments')[0]);

    $.ajax({
        url: "/api/departments/",
        context: document.body
    }).done(function (data) {
        departmentModel.departments(data);
    });
});



