var send_data = {}	
$(document).ready(function(){
    reset();

    getData();

    $("#authors").change(function(e){
        if(this.value == "")
            send_data['author'] = "";
        else
            send_data['author'] = this.value;
        
        getData();
    });

    $('#categories').change(function(e){
        if(this.value == "")
            send_data['category'] = "";
        else
            send_data['category'] = this.value;
        
        getData();
    });

    $("#display_all").click(function(){
        reset();
        getData();
    })
})

function reset() {
	send_data['author'] = "";
	send_data['category'] = "";
}

function printData(response) {
	$("#book_info table tbody").html("");
	if(response["results"].length > 0){
		$.each(response["results"], function (a, entry){
			var cat = entry.categories.flatMap(c => c.category_name).join();
			var aut = entry.authors.flatMap(a => a.name + " " + a.surname).join();

			$("#book_info table tbody").append(`<tr>
				<td>${entry.title.slice(0,30) || "-"}</td>
				// <td>${aut || "-"}</td>
				// <td>${cat || "-"}</td>
				<td>${entry.description.length > 200 ? entry.description.slice(0,200)  + "..." : entry.description|| "-"}</td>
				</tr>`);
		})

	}
	let prev_url = response["previous"];
    let next_url = response["next"];

    if (prev_url === null) {
        $("#previous").addClass("disabled");
        $("#previous").prop('disabled', true);
    } else {
        $("#previous").removeClass("disabled");
        $("#previous").prop('disabled', false);
    }
    if (next_url === null) {
        $("#next").addClass("disabled");
        $("#next").prop('disabled', true);
    } else {
        $("#next").removeClass("disabled");
        $("#next").prop('disabled', false);
    }
    $("#previous").attr("url", response["previous"]);
    $("#next").attr("url", response["next"]);

}



$("#next").click(function () {
    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (response) {
            printData(response);
        },
        error: function(response){
            console.log(response)
        }
    });
})

$("#previous").click(function () {
    let url = $(this).attr("url");
    if (!url)
        $(this).prop('all', true);

    $(this).prop('all', false);
    $.ajax({
        method: 'GET',
        url: url,
        success: function (response) {
            printData(response);
        },
        error: function(response){
            console.log(response)
        }
    });
})

function getData() {
    let url = $("#book-info").attr("url");

	$.ajax({
		method: 'GET',
		url: url,
		data: send_data,
		success: function(response) {
			console.log(send_data);
			printData(response);
		},
		error: function (response) {
			console.log(response);
		}
	});
}