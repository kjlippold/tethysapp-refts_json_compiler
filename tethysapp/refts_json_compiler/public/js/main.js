function addFileToTable(fileName) {
    var table = document.getElementById("table-refts-files");
    var row = table.insertRow(-1);
    var cellFile = row.insertCell(0);
    var cellStatus = row.insertCell(1);
    var cellAction = row.insertCell(2);
    cellFile.innerHTML = fileName;
    cellStatus.innerHTML = "<img src='/static/refts_json_compiler/images/working.gif' alt='Working' style='width:50px;height:40px;'>";
    cellAction.innerHTML = "<input id='checkBox' type='checkbox'>";
}

var onClickUploadFiles;
var $btnUploadFiles;


$btnUploadFiles = $('#btn-upload-files');


onClickUploadFiles = function () {
    var files = document.getElementById("input-upload-files").files;
    for (var i = 0; i < files.length; i++)
    {
        addFileToTable(files[i].name);
    }
    for (var n = 0; n < files.length; n++)
    {
        var data = new FormData();
        data.append('file', files[n]);
        $.ajax({
            url: '/apps/refts-json-compiler/convert-files/',
            type: 'POST',
            data: data,
            dataType: 'json',
            processData: false,
            contentType: false
        });
    }
};


$btnUploadFiles.on('click', onClickUploadFiles);