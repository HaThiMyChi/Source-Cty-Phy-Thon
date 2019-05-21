(function( $ ) {
    $.fn.createTable = function() {
        initTemplate(this);
        loadSelect(this);
        loadSearch(this);
        add(this);
        changeEdit(this);

        var current_page = 1;
        var  page_size = $(this).find('.single').val();
//        var key_word = $('#myInput').val();

        loadPage(this,current_page,page_size);
    };
}( jQuery ));

    $(function() {
        initTemplate = function(obj) {
           var html = '<div class="row  search-div">';
            html += '<div class="col-sm-12 col-md-6">';
            html += '<div class="dataTables_length bs-select" id="dtBasicExample_length">';
            html += '<div class="label--top">Show';
            html += '</div>';
            html += '<select  class="single form-control" name="dtBasicExample_length" aria-controls="dtBasicExample" class="custom-select custom-select-sm form-control form-control-sm">';
            html += '<option value="5">5</option>';
            html += '<option value="7">7</option>';
            html += '<option value="10">10</option>';
            html += '<option value="15">15</option>';
            html += '</select>';
            html += '</div>';
            html += '</div>';
            html += '<div class="input-group col-sm-4 offset-ms-4">';
            html += '<input id="myInput" type="text" class="form-control" aria-label="Recipient\'s username" aria-describedby="button-addon2">';
            html += '<div class="input-group-append">';
            html += '<select class="custom-select">';
            html += '<option value="all">All</option>'
            html += '<option value="name">Name</option>'
            html += '<option value="age">Age</option>'
            html += '<option value="national">National</option>'
            html += '<option value="position">Position</option>'
            html += '<option value="salary">Salary</option>'
            html += '</select>'
            html += '<button class="btn btn-secondary" type="search" id="button-search">Search</button>';
            html += '</div>';
            html += '</div>';
            html += '</div>';
            html += '<table id="datatable" class="table">';
            html += '<thead>';
            html += '<tr>';
            html += '<th scope="col">ID</th>';
            html += '<th scope="col">Tên cầu thủ</th>';
            html += '<th scope="col">Tuổi</th>';
            html += '<th scope="col">Quốc tịch</th>';
            html += '<th scope="col">Vị trí</th>';
            html += '<th scope="col">Lương</th>';
            html += '<th scope="col">Edit</th>';
            html += '<th scope="col">Delete</th>';
            html += '</tr>';
            html += '</thead>';
            html += '<tbody>';
            html += '</tbody>';
            html += '</table>';

            html += '<tfoot>';
            html += '<tr>';
            html += '<td colspan="8">';
            html += '<button class="btn btn-primary" id="button" data-toggle="modal" data-target="#exampleModal" data-whatever="@getbootstrap">Thêm cầu thủ</button>';
            html += '</td>';
            html += '</tr>';
            html += '</tfoot>';
            html += '<nav aria-label="Page navigation example" class="page">';
            html += '<ul id="test" class="pagination">';
            html += '</ul>';
            html += '</nav>';

            $(obj ).html(html);
        }
    });

    $(function() {
        loadPage = function(obj,current_page,page_size) {
           var url = '/getlist?page='+current_page+'&page_size='+page_size;
            $.ajax({
            url: url,
            method: "GET",
            success: function(data) {
            var res = JSON.parse(data);
            var html = '';
            html += loadTable(res.players);
            $(obj ).find('table tbody').html(html);
                buildPaging(obj,res);
                edit();
                }
            });
        };
    });

    $(function() {
        loadSearchIndex = function(obj, current_page, page_size, key_word, type) {
           var url = '/search';
            $.ajax({
            url: url,
            method: "POST",
            data: {page: current_page, page_size: page_size, key_word: key_word, type: type},
            success: function(data) {
                var res = JSON.parse(data);
                var html = '';
                html += loadTable(res.players);
                $(obj ).find('table tbody').html(html);
                buildPaging(obj,res);
                }
            });
        };
    });

    $(function() {
        loadTable = function(players){
            var html='search no data, please  search again!';
                for (var i = 0; i < players.length; i++) {
                    var player = players[i];
                    html += '<tr>';
                    html += '<td>' + player.id + '</td>';
                    html += '<td>' + player.name + '</td>';
                    html += '<td>' + player.age + '</td>';
                    html += '<td>' + player.national + '</td>';
                    html += '<td>' + player.position + '</td>';
                    html += '<td>' + player.salary + '</td>';
//                    html += '<td><a href="/edit?id='+ player.id +'">Edit</a></td>';
                    html += '<td><button type="button" class="btn btn-primary btn-edit" data-toggle="modal" data-target="#exampleModal1">Edit</button></td>';
//                    html += '<td><a href="/remove?id='+ player.id +'">Delete</a></td>';
                    html += '<td><button  type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal2">Delete</button></td>';
                    html += '</tr>'
                 }

                return html;
        };
    });

    $(function(){
        buildPaging = function(obj,res) {
            var html ='';
                for(var i = 1 ;i< res.number_page ; i++){
                    if(res.current_page == i){
                         current_page = res.current_page;
                        html += '<li class="page-item"><a class="page-link page-selected" href="#">'+i+'</a></li>';
                    }else{
                        html += '<li class="page-item"><a class="page-link" href="#">'+i+'</a></li>';
                    }
                }
                $(obj).find('.pagination').html(html);
                    $(obj).find('li a').click(function(){
                        var page = $(this).html();
                        var page_size = $(obj).find('.single').val();
//                      var key_word = $('#myInput').val();
                        loadPage(obj,page,page_size);
                 });
        }
    });

    $(function(){
        loadSelect = function (obj) {
            $(obj).find('.single').change(function(){
              var page_size = $(this).val();
//            page_size = singleValues;
//              var key_word = $('#myInput').val();
              var current_page = $(obj).find('.pagination .page-selected').html();
              loadPage(obj, current_page,page_size);
            });
        }
    });

    $(function(){
        loadSearch = function(obj){
            $('#button-search').click(function(){
                var  page_size = $(obj).find('.single').val();
                var key_word = $('#myInput').val();
//              console.log(typeof(key_word));
                var type = $('.custom-select').val();
                loadSearchIndex(obj, 1, page_size, key_word, type);
            });
        }
    });

    $(function(){
        showAdd = function(name, age, national, position, salary) {
           var url = '/add';
            $.ajax({
            url: url,
            method: "POST",
            data: {name: name, age: age, national: national, position: position, salary: salary},
//            success: function(data) {
//               console.log(data);
//                var res = JSON.parse(data);
//                var html = '';
//                html += loadTable(res.players);
//                $(obj ).find('table tbody').html(html);
//                buildPaging(obj,res);
//                }
//            error: function(jqXHR, textStatus, errorThrown){
//               alert('jqXHR:' + jqXHR + ' textStatus: '+ textStatus + ' errorThrown: '+ errorThrown);
//            }
            });

        };
    });

    $(function(){
        add = function(){
            $('#btn-add').click(function(){
                var name = $('#name').val();
                var age = $('#age').val();
                var national = $('#national').val();
                var position = $('#position').val();
                var salary = $('#salary').val();
                showAdd(name, age, national, position, salary );
            });
        }
    });

    $(function(){
       showEdit = function(id, name, age, national, position, salary) {
           //var url = '/edit';
            $.ajax({
            url: '/edit',
            method: "POST",
            data: {id: id, name: name, age: age, national: national, position: position, salary: salary},
//            success: function(data) {
//                console.log(data);
//                }
            });
        };
    });

   $(function(){
        edit = function(){
             $('#datatable').on('click', '.btn-edit',function(){
//                var id = $(this).parent().parent().find('th');
                var currentRow=$(this).closest("tr");
                var id=currentRow.find("td:eq(0)").text();
                var name=currentRow.find("td:eq(1)").text()
                var age=currentRow.find("td:eq(2)").text();
                var national=currentRow.find("td:eq(3)").text();
                var position=currentRow.find("td:eq(4)").text();
                var salary=currentRow.find("td:eq(5)").text();
//                var name = $(this).parent().parent().find('td').val();
//
//                var age = $(this).parent().parent().find('td');
//                var national = $(this).parent().parent().find('td');
//                var position = $(this).parent().parent().find('td');
//                var salary = $(this).parent().parent().find('td');
                $('#Id1').val(id);
                $('#name1').val(name);
                $('#age1').val(age);
                $('#national1').val(national);
                $('#position1').val(position);
                $('#salary1').val(salary);
//              alert(name.html());
            });
        }
    });

    $(function(){
        changeEdit = function(){
            $('#btnEdit').click(function(){
                var id =  $('#Id1').val();
                var name = $('#name1').val();
                var age = parseInt($('#age1').val(), 10);
                var national = $('#national1').val();
                var position = parseInt($('#position1').val());
                var salary = parseInt($('#salary1').val());
//                var currentRow=$(this).closest("tr");
//                var id=currentRow.find("td:eq(0)").text();
                showEdit(id, name, age, national, position, salary );
            });
        }
    });



$(document).ready(function() {
    $('#table').createTable();
    return;

});