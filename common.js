// document.onload({});

// $('#new').on('click', function() {

// 	$.ajax({
// 		url:"/create?render=yes&company=kuku", 
// 		type:'get',
// 		success: function(response){
// 			console.log(response);
// 			window.location = '/create?render=yes';
// 		}
// 	});
// });

$('#recordForm').submit(function (e) {
	// body...
	e.preventDefault();
	var truck_num = $('#truckNum').val();
	var company = $('#compName').val();
	var bon_num = $('#bonNum').val();
	var expenses = $('#exps').val();
	var income = $('#income').val();
	$.ajax({
		url:"/create?truck_num="+truck_num+"&company='"+company+"'&bon_num="+bon_num+"&expenses="+expenses+"&income="+income, 
		type:'get',
		// data: {truck_num:truck_num,company:company,bon_num:bon_num,expenses:expenses,income:income}
		success: function(response){
			window.location = '/status?title='+response.title+'&msg='+response.msg;
		}
	});
}

);

function goHome(){
	window.location='/';
}

function viewAll(){
	// alert('kuku');
	$.ajax({
		url: "/getRecord?all=yes",
		type: 'get',
		success: function(data){
			alert(data.responseText);
			var data = data;
			// window.location = '/viewAll';
			alert('kuku');
			$.each(JSON.parse(data), function(){
				$('#records > tbody:last-child').append("<tr id='"+this.id+"'><td class='tabcols firstRow'>"+this.truck_num+"<td><td class='tabcols'>"+this.company+"<td><td class='tabcols'>"+this.bon_num+"<td><td class='tabcols'>"+this.expenses+"<td><td class='tabcols'>"+this.income+"<td><td class='tabcols'><a href='/view?id="+this.id+"'>view</a></br><a href='/del?id="+this.id+"'></a><td></tr>");
				// alert(this.id);
				// $.each(this, function(k, v){
				// });
			});
			console.log(data)
		}
	});
}